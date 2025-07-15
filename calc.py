from typing import Tuple

import gradio as gr


def deepmind_flops(
    n_layer: int,
    d_model: int,
    d_ff: int,
    d_attn: int,
    n_ctx: int,
    n_vocab: int,
    n_heads: int,
) -> int:
    embeddings = 2 * n_ctx * n_vocab * d_model
    attn_qkv = 2 * n_ctx * 3 * d_model * (d_attn * n_heads)
    attn_logits = 2 * n_ctx * n_ctx * (d_attn * n_heads)
    attn_softmax = 3 * n_heads * n_ctx * n_ctx
    attn_reduce = 2 * n_ctx * n_ctx * (d_attn * n_heads)
    attn_project = 2 * n_ctx * (d_attn * n_heads) * d_model
    ff = 2 * n_ctx * (d_model * d_ff + d_model * d_ff)
    logits = 2 * n_ctx * d_model * n_vocab

    params = (
        embeddings / n_ctx / 2,
        (n_layer * (attn_qkv + attn_project + ff)) / n_ctx / 2,
        logits / n_ctx / 2,
    )

    return (
        embeddings,
        attn_qkv * n_layer,
        attn_logits * n_layer,
        attn_softmax * n_layer,
        attn_reduce * n_layer,
        attn_project * n_layer,
        ff * n_layer,
        logits,
    ), params


def calculator(
    n_layer: int,
    d_model: int,
    n_heads: int,
    n_vocab: int,
    ff_ratio: int,
    n_ctx: int,
    n_tokens: int,
    incl_embed: bool,
    fwd_only: bool,
) -> Tuple[int, int, int]:
    d_attn = d_model // n_heads
    if d_model % n_heads != 0:
        raise gr.Error("d_model must be divisible by n_heads")
    d_ff = d_model * ff_ratio

    flops_terms, params = deepmind_flops(
        n_layer, d_model, d_ff, d_attn, n_ctx, n_vocab, n_heads
    )

    if incl_embed:
        flops_per_sequence = sum(flops_terms)
        params = sum(params)
    else:
        flops_per_sequence = sum(flops_terms[1:])
        params = sum(params[1:])

    flops_per_token = flops_per_sequence / n_ctx

    n_tokens_flops = flops_per_token * n_tokens

    if not fwd_only:
        flops_per_sequence *= 3
        flops_per_token *= 3
        n_tokens_flops *= 3

    return params, flops_per_sequence, flops_per_token, n_tokens_flops


with gr.Blocks() as iface:
    gr.Markdown(
        "Calculate how many FLOPs a Transformer language model uses with the method described in [DeepMind's Chinchilla scaling law paper](https://arxiv.org/abs/2203.15556) (see Appendix F)."
    )
    with gr.Row():
        with gr.Column():
            gr.Markdown("#### Architecture details")
            n_layer = gr.Number(label="Number of layers (n_layer)")
            d_model = gr.Number(label="Model dimensions (d_model)")
            n_heads = gr.Number(label="Number of attention heads per layer (n_heads)")
            n_vocab = gr.Number(label="Vocabulary size (n_vocab)")
            ff_ratio = gr.Number(value=4, label="Feedforward ratio")
            gr.Markdown("#### Data details")
            n_ctx = gr.Number(label="Sequence length (n_ctx)")
            n_tokens = gr.Number(
                value=0,
                label="Total number of training tokens (n_tokens) (optional)",
            )
            gr.Markdown("#### Settings")
            incl_embed = gr.Checkbox(value=True, label="Include embeddings")
            fwd_only = gr.Checkbox(
                value=False, label="Calculate FLOPs for only forward pass"
            )

            btn = gr.Button(value="Enter", variant="primary")

        with gr.Column():
            gr.Markdown("#### Output")
            params = gr.Number(label="Model parameters")
            flops_per_sequence = gr.Number(label="FLOPs per sequence")
            flops_per_token = gr.Number(label="FLOPs per token")
            n_tokens_flops = gr.Number(label="Total FLOPs for n_tokens")

    btn.click(
        calculator,
        inputs=[
            n_layer,
            d_model,
            n_heads,
            n_vocab,
            ff_ratio,
            n_ctx,
            n_tokens,
            incl_embed,
            fwd_only,
        ],
        outputs=[params, flops_per_sequence, flops_per_token, n_tokens_flops],
    )

    gr.Markdown("### GPT-3 model family examples")
    gr.Markdown(
        "In order are the 125M, 350M, 1.3B, 2.7B, 6.7B, 13B, 30B, 66B, and 175B parameter variants."
    )
    gr.Examples(
        [
            [12, 768, 12, 50257, 4, 4096, 0, True, False],
            [24, 1024, 16, 50257, 4, 4096, 0, True, False],
            [24, 2048, 32, 50257, 4, 4096, 0, True, False],
            [32, 2560, 32, 50257, 4, 4096, 0, True, False],
            [32, 4096, 32, 50257, 4, 4096, 0, True, False],
            [40, 5120, 40, 50257, 4, 4096, 0, True, False],
            [48, 7168, 56, 50257, 4, 4096, 0, True, False],
            [64, 9216, 72, 50257, 4, 4096, 0, True, False],
            [96, 12288, 96, 50257, 4, 4096, 0, True, False],
        ],
        [
            n_layer,
            d_model,
            n_heads,
            n_vocab,
            ff_ratio,
            n_ctx,
            n_tokens,
            incl_embed,
            fwd_only,
        ],
        [params, flops_per_sequence, flops_per_token, n_tokens_flops],
        calculator,
        cache_examples=False,
    )

iface.launch()