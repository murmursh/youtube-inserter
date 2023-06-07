import os
import zipfile
import shutil

def antifingerprint_extention(vendor, unmask_vendor_webgl, renderer, unmasked_renderer_webgl, version, shading_language_version, move_to):
    data = {
        "UNMASKED_VENDOR_WEBGL": unmask_vendor_webgl,
        "RENDERER": renderer,
        "VENDOR": vendor,
        "UNMASKED_RENDERER_WEBGL": unmasked_renderer_webgl,
        "VERSION": version,
        "SHADING_LANGUAGE_VERSION": shading_language_version
    }
    with open("extentions/fingerprint_defender/webgl.pjs", 'r') as f:
        with open("extentions/fingerprint_defender/webgl.js", 'w') as f2:
            f2.write(f.read() % data)

    shutil.copytree("extentions/fingerprint_defender", os.path.join(move_to, "fingerprint_defender"), dirs_exist_ok=True)
