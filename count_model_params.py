"""Count trainable parameters for TSformer-VO presets."""

from build_model import build_model, count_parameters


def make_args_and_model_params(window_size: int):
    args = {
        "window_size": window_size,
        "checkpoint": None,
        "pretrained_ViT": False,
        "checkpoint_path": ".",
    }
    model_params = {
        "dim": 384,
        "image_size": (192, 640),
        "patch_size": 16,
        "attention_type": "divided_space_time",
        "num_frames": window_size,
        "num_classes": 6 * (window_size - 1),
        "depth": 12,
        "heads": 6,
        "dim_head": 64,
        "attn_dropout": 0.1,
        "ff_dropout": 0.1,
        "time_only": False,
    }
    return args, model_params


def main():
    for window_size in (2, 3, 4):
        args, model_params = make_args_and_model_params(window_size)
        model, _ = build_model(args, model_params)
        params = count_parameters(model)
        print(f"TSformer-VO-{window_size - 1} (Nf={window_size}): {params:,} ({params / 1_000_000:.2f}M)")


if __name__ == "__main__":
    main()
