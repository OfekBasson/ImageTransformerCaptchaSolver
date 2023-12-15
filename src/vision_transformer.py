from torchvision.models.vision_transformer import Encoder
import torch.nn as nn
import torch

class VisionTransformer(nn.Module):
    def __init__(self, image_size, patch_size, num_classes, num_layers, num_heads, hidden_dim, mlp_dim, dropout, attention_dropout):
        super().__init__()
    
        seq_length = int(((image_size/patch_size) ** 2)) + 1

        self.unfold = nn.Unfold(kernel_size=patch_size, stride=patch_size)
        self.linear = nn.Linear((patch_size ** 2) * 3, hidden_dim)
        self.class_embedding = nn.Parameter(torch.randn(1, 1, hidden_dim))
        self.positional_encoding = nn.Parameter(torch.randn(1, seq_length, hidden_dim))
        self.encoder = Encoder(
        seq_length=seq_length,
        num_layers=num_layers,
        num_heads=num_heads,
        hidden_dim=hidden_dim,
        mlp_dim=mlp_dim,
        dropout=dropout,
        attention_dropout=attention_dropout
        )       
        self.MLP = nn.Linear(hidden_dim, num_classes)

        self.data_tracking_for_visualization = {"train": {
            "acc": [],
            "loss": []
        }, "val": {
            "acc": [],
            "loss": []
        }}

    def forward(self, images):
        images = images[:,:3,:,:]
        images = self.unfold(images).transpose(1, 2)
        images = self.linear(images)
        images = torch.cat((self.class_embedding.expand(images.shape[0], 1, images.shape[2]), images), 1)
        images = torch.add(images, self.positional_encoding.expand(images.shape))
        images = self.encoder(images)

        return self.MLP(images[:,0,:])

