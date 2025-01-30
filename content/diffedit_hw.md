Title: Implementing DiffEdit
Date: 2024-07-24 14:55
Category: Dailies
Status: draft
Today we'll work on [lesson 11's](https://course.fast.ai/Lessons/lesson11.html) homework: implementing the [DiffEdit](https://arxiv.org/pdf/2210.11427) paper. In the lesson we went over the paper, and saw that the method is fairly straightforward. In fact, I was tempted to skip this, but then I realized this is classic case of the illusion of knowledge: I think it's easy to implement, but when it comes to it, there are a lot of small details I am not sure about. It's like thinking a song is easy to play on the piano, but when you actually try to play it you see the the chord changes are actually not that familiar and you stutter.

We start with the manual pipeline code from one of the previous lectures. It's quite short

```python
import torch
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, UNet2DConditionModel
from diffusers import LMSDiscreteScheduler
from IPython.display import display
from tqdm.auto import tqdm
from PIL import Image

prompts = [
    'a photograph of an astronaut riding a horse',
    'an oil painting of an astronaut riding a horse in the style of grant wood'
]
height = 512
width = 512
num_inference_steps = 70
guidance_scale = 7.5
batch_size = 1
beta_start,beta_end = 0.00085,0.012

tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14", torch_dtype=torch.float16)
text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14", torch_dtype=torch.float16).to("cuda")
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-ema", torch_dtype=torch.float16).to("cuda")
unet = UNet2DConditionModel.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="unet", torch_dtype=torch.float16).to("cuda")
scheduler = LMSDiscreteScheduler(beta_start=beta_start, beta_end=beta_end, beta_schedule="scaled_linear", num_train_timesteps=1000)

def text_enc(prompts, maxlen=None):
    if maxlen is None: maxlen = tokenizer.model_max_length
    inp = tokenizer(prompts, padding="max_length", max_length=maxlen, truncation=True, return_tensors="pt")
    return text_encoder(inp.input_ids.to("cuda"))[0].half()

def mk_img(t):
    image = (t/2+0.5).clamp(0,1).detach().cpu().permute(1, 2, 0).numpy()
    return Image.fromarray((image*255).round().astype("uint8"))

def mk_samples(prompts, g=7.5, seed=100, steps=70):
    bs = len(prompts)
    text = text_enc(prompts)
    uncond = text_enc([""] * bs, text.shape[1])
    emb = torch.cat([uncond, text])
    if seed: torch.manual_seed(seed)

    latents = torch.randn((bs, unet.in_channels, height//8, width//8))
    scheduler.set_timesteps(steps)
    latents = latents.to("cuda").half() * scheduler.init_noise_sigma

    for i,ts in enumerate(tqdm(scheduler.timesteps)):
        inp = scheduler.scale_model_input(torch.cat([latents] * 2), ts)
        with torch.no_grad(): u,t = unet(inp, ts, encoder_hidden_states=emb).sample.chunk(2)
        pred = u + g*(t-u)
        latents = scheduler.step(pred, ts, latents).prev_sample

    with torch.no_grad(): return vae.decode(1 / 0.18215 * latents).sample

images = mk_samples(prompts)
```

Some imports, loading models, some hyperparams. Inference takes place in `mk_samples`, and this is where we'll introduce our changes.

## How DiffEdit works
So what's the idea behind DiffEdit? we have the following chart from the paper
<p style="width:100%; margin:auto">
  <img src="{static}images/diffedit_flow.png" />
</p>
<!--![[diffedit_flow.png]]-->

The notation seems to be:
- $R$ - the reference text, ie the text that describes the original image.
- $Q$ - the query, ie what describes the new image we wish to have.
- $x_{t}$ - the original image in diffusion step $t$.
- $y_t$ - the modified image in diffusion step $t$.

### Step 1: Compute a mask
In the first step, we introduce noise into the image. We then feed the noised image to the model with the two different prompts, once with $R$ and once with $Q$. We then look at the difference between the predicted noises. The idea is, where these noises differ is where a horse differs from a zebra. For example, for a pixel in the background it doesn't matter whether the animal is a horse or a zebra, therefore the noise there will be the same across the queries. On the other hand, a pixel on the animal's body does depend on the query: a horse will be reddish while a zebra black/white.

The mask is binarized, that means that we choose a threshold and every pixel where the difference is above that threshold becomes `True`.

**Qs:**
- How much noise is introduced? what step of the diffusion do we reach?
- How is the noise introduced? probably the scheduler
- Do we compute one denoising step? I think so
- How is the difference normalized?


Let's implement this part. Stuff to do:
- Load an image
- Encode it using vae (stable diffusion acts in latent space)
- Noise it with scheduler
	- generate standard gaussian noise
	- choose a timestep

<hr>

Yep, this is definitely good practice, so I'm going to be fairly descriptive. For loading an image, we first use the PIL library:
```python
from PIL import Image

im = Image.open(path)
```
To convert it to a tensor we use the `torchvision` library
```python
from torchvision import transforms
							
im_t = transforms.ToTensor()(im.convert("RGB"))
```
`im_t` is now a `float32` tensor with shape `(3, 512, 512)` (so color channels are the first index as is torch's convention). The values range from 0 to 1. This is important as the autoencoder expects images to be within -1 and 1, so we have to scale the image
```python
im_t = (im_t - .5) * 2
```

Now to encode using the autoencoder, it's fairly straightforward.
```python
with torch.no_grad():
    enc = vae.encode(im_t).latent_dist.mean
    dec = vae.decode(enc).sample
```
We look at the original vs the decoded for sanity (I found some bugs that way)
<!--![[omri_orig.png]]![[omri_dec.png]]-->
<div style="display: flex; justify-content: center;">
  <div style="text-align: center; margin: 0 10px;">
    <img src="{static}images/omri_orig.png" alt="Original Image" style="max-width: 100%; height: auto;">
    <div>Original</div>
  </div>
  <div style="text-align: center; margin: 0 10px;">
    <img src="{static}images/omri_dec.png" alt="Decoded Image" style="max-width: 100%; height: auto;">
    <div>Decoded</div>
  </div>
</div>
there is a twist though: SD scales the encoding so we need to remember to scale it down and up.
```python
with torch.no_grad():
    enc =  0.18215 * vae.encode(im_t).latent_dist.mean
    dec = vae.decode(1 / 0.18215 * enc).sample
```

We're going to noise it with the scheduler. 
```python
scheduler.set_timesteps(steps)
noise = torch.randn(enc.shape)

step = 64 # the diffusion step we take
timesteps = torch.tensor([scheduler.timesteps[step]])
noisy_image = scheduler.add_noise(enc, noise, timesteps)
```
If we decode the noisy image we get back
<!--![[omri_noisy.png]]-->
<p style="width:50%; margin:auto">
  <img src="{static}images/omri_noisy.png" />
</p>
We will figure out later a proper step choice. Now for the denoising step, this is where things get fuzzy and uncertain. What I did so far is
```python
inp = scheduler.scale_model_input(torch.cat([noisy_image] * 2), timesteps)
with torch.no_grad():
	r,q = unet(inp, timesteps, encoder_hidden_states=emb).sample.chunk(2)
```
`r` and `q` should be the predicted noises. The question I have now is whether we can visualize the mask. The tricky part is it's in the latent space, so the mapping the pixels is not straightforward. Maybe it's time to read the paper.

> In our algorithm, we use a Gaussian noise with strength 50% (see analysis in Appendix A.1), remove extreme values in noise predictions and stabilize the effect by averaging spatial differences over a set of `n` input noises, with `n=10` in our default configuration. The result is then rescaled to the range \[0, 1\], and binarized with a threshold, which we set to 0.5 by default.

Here's the modifications I did based on that (untouched lines omitted)
```python
n_noise = 10
mask_thresh = 0.5

# change noise to have n_noise copies
noise = torch.randn(n_noise, *enc.shape[1:]).cuda().half()

# change emb to have n_noise copies
emb = torch.cat([emb[0][None,...]] * n_noise + [emb[1][None,...]] * n_noise)
with torch.no_grad():
    r,q = unet(inp, timesteps, encoder_hidden_states=emb).sample.chunk(2)

# calculate mask according to description
mask = (r - q).mean(dim=0).abs()
mask = (mask - mask.min()) / (mask.max() - mask.min())
mask = mask > mask_thresh
```

Looking at the masks, it kinda looks reasonable, pixels are located next to the hands, but it's quite sparse. I guess we'll see.
<!--![[mask_channels.png]]-->
<p style="width:80%; margin:auto">
  <img src="{static}images/mask_channels.png" />
</p>

Okay, on to step two.

### Step 2: Encode with DDIM until encoding ratio r
What the hell is $r$? from the paper
> In the remainder of the paper, we parameterize the timestep t to be between 0 and 1, so that t = 1 corresponds to T steps of diffusion in the original formulation.

>as proposed by Song et al. (2021), we can also use this ODE to encode an image $x_0$ onto a latent variable $x_r$ for a timestep $r\leq 1$

and
>In the remainder of the paper, we refer to this encoding process as DDIM encoding, we denote the corresponding function that maps $x_0$ to $x_r$ as $E_r$ and refer to the variable $r$ as the encoding
ratio.

So $r$ is the time step. I wonder if the mask phase and decoding phase have to be identical? probably not, since the "strength" of the noise is 50%, if only I knew what that means.

<hr>

Let's get things straight for a second, what are all these letters standing for? according to the paper, the forward diffusion is defined as
$$
x_t = \sqrt{\alpha_t}x_0+\sqrt{1-\alpha_t}\varepsilon
$$
where $\varepsilon\sim \mathcal N(0, I)$. What would be 50% strength then? when $\alpha_t=1-\frac{1}{2^2}$? 

<hr>

Putting that aside for now, let's get the second step implemented.  Working on this

```python
r = 0.3
enc_step = int(steps * (1-r))
enc_step2 = torch.tensor([scheduler.timesteps[:enc_step]]).cuda()
enc_r = scheduler.add_noise(enc, noise[:1], enc_step2)
# latents = latents.to("cuda").half() * scheduler.init_noise_sigma

for i,ts in enumerate(tqdm(scheduler.timesteps[enc_step:])):
    inp = scheduler.scale_model_input(torch.cat([latents] * 2), ts)
```