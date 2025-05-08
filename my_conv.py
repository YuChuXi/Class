import torch
import torch.nn.functional as F


def myconv(image, kernel):
    stride = 2
    output = torch.zeros((3, 3, 2))

    for k in range(2):
        for y in range(3):
            for x in range(3):
                y_start = y * stride
                y_end = y_start + 3
                x_start = x * stride
                x_end = x_start + 3

                window = image[y_start:y_end, x_start:x_end, :]
                conv_result = torch.sum(window * kernel[k], dim=(0,1,2))
                output[y, x, k] = conv_result

    return output


image = torch.rand((7, 7, 3))
kernel = torch.rand((2, 3, 3, 3))

custom_result = myconv(image, kernel)
print("my", custom_result, custom_result.shape)

torch_result = F.conv2d(image.permute(2, 0, 1).unsqueeze(0), kernel.permute(0, 3, 1, 2), stride=(2,2)).squeeze(0).permute(1, 2, 0)

print("torch", torch_result, torch_result.shape)
"""

my tensor([[[7.3543, 7.1042],
         [6.3866, 6.2882],
         [7.6394, 7.8611]],

        [[6.6815, 6.2210],
         [6.1381, 5.8996],
         [7.1033, 6.9617]],

        [[7.2261, 6.8250],
         [5.6021, 6.6140],
         [5.2118, 5.2411]]]) torch.Size([3, 3, 2])
torch tensor([[[7.3543, 7.1042],
         [6.3866, 6.2882],
         [7.6394, 7.8611]],

        [[6.6815, 6.2210],
         [6.1381, 5.8996],
         [7.1033, 6.9617]],

        [[7.2261, 6.8250],
         [5.6021, 6.6140],
         [5.2118, 5.2411]]]) torch.Size([3, 3, 2])
         
"""