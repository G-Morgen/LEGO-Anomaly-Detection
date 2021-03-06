import argparse
import train

train_commands = [
    # anoCAE
    "-d LEGO_light/SV -a anoCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
    # baselineCAE
    "-d LEGO_light/SV -a baselineCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
    # inceptionCAE
    "-d LEGO_light/SV -a inceptionCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
    # mvtecCAE
    "-d LEGO_light/SV -a mvtecCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
    # resnetCAE
    "-d LEGO_light/SV -a resnetCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
    # skipCAE
    "-d LEGO_light/SV -a skipCAE -b 8 -l mssim -c rgb -e 60 -r custom --inspect",
]


parser = train.create_parser()
for command in train_commands:
    args_list = command.split(" ")
    args = parser.parse_args(args_list)
    try:
        train.main(args)
    except Exception:
        pass

