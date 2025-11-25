from enum import Enum

class SigText(Enum):
    OggS = "ogg"
    ID3 = "mp3_id3"
    FF_FB = "mp3_fffb"
    RIFF = "wav"
    fLaC = "flac"
    PNG = "png"
    FF_D8_FF = "jpg"
    GIF87a = "gif"
    GIF89a = "gif"
    BM = "bmp"
    KTX = "ktx"
    DDS = "dds"
    PVR_03 = "pvr"
    PDF = "pdf"
    PK_03_04 = "zip"
    RBXM = "rbxm"
    RBXL = "rbxl"
    other = "other"

class FileSig(Enum):
    ogg      = b"OggS"
    mp3_id3  = b"ID3"
    mp3_fffb = b"\xFF\xFB"
    wav      = b"RIFF"
    flac     = b"fLaC"
    png      = b"\x89PNG\r\n\x1a\n"
    jpg      = b"\xFF\xD8\xFF"
    gif87a   = b"GIF87a"
    gif89a   = b"GIF89a"
    bmp      = b"BM"
    ktx      = b"\xABKTX"
    dds      = b"DDS "
    pvr_03   = b"PVR\x03"
    pdf      = b"%PDF"
    zip      = b"PK\x03\x04"
    rbxm     = b"<roblox!"
    rbxl     = b"<roblox!"
    other    = b"other"

broad = {
    SigText.OggS: "sound",
    SigText.ID3: "sound",
    SigText.FF_FB: "sound",
    SigText.RIFF: "sound",
    SigText.fLaC: "sound",
    SigText.PNG: "image",
    SigText.FF_D8_FF: "image",
    SigText.GIF87a: "image",
    SigText.GIF89a: "image",
    SigText.BM: "image",
    SigText.KTX: "image",
    SigText.DDS: "image",
    SigText.PVR_03: "image",
    SigText.PDF: "document",
    SigText.PK_03_04: "archive",
    SigText.RBXM: "model",
    SigText.RBXL: "model",
    SigText.other: "other"
}