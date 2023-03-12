**WARNING** This library is still under development and intended for experimental purposes only.

# COVID Vaccination Certificate QR code decoder

```sh
python3 ./webcam_capture_QR_code.py | python3 ./covid-certificate-qr-decoder.py
```

* The `webcam_capture_QR_code.py` script is a QR-code scanner. It turns on your webcam, waits for you to show it a QR-code, decodes it, extracts the data, prints it out, and exits. If your QR-code is a COVID vaccination certificate, the output will be a base45 string that you can recognize by the `HC1:` prefix.

* The `covid-certificate-qr-decoder.py` script can decode a COVID vaccination certificate base45 string (recognizable by the `HC1:` prefix), decompress the data, decode it again as a COSE message based on the CBOR tag, deserialize the resulting bytestring, print it out, and exit. This script works in pair with its best buddy script `webcam_capture_QR_code.py`.

## Installation

1. Clone the repository.
2. Install dependencies: `python3 -m pip -r requirements.txt`

## Usage

Launch one or the other script, or both, or any of them in combination with other shell commands:

```sh
# scan a QR-code with your webcam and pipe the base45 string to the decoder:
python3 ./webcam_capture_QR_code.py | python3 ./covid-certificate-qr-decoder.py

# or decode any base45 string:
echo "HC1:........." | python3 ./covid-certificate-qr-decoder.py

# or scan any QR-code with your webcam:
python3 ./webcam_capture_QR_code.py
```

## Technical resources

- API spec:
    - https://github.com/eu-digital-green-certificates/dgca-issuance-web/blob/main/src/generated-files/dgc-combined-schema.d.ts
- Test data:
    - https://github.com/eu-digital-green-certificates/dgc-testdata/
- Encode data into a new COVID Certificate base45 string:
    - https://github.com/eu-digital-green-certificates/dgca-issuance-web/blob/main/src/misc/edgcProcessor.tsx
- COVID certificate examples:
    - https://github.com/admin-ch/CovidCertificate-Examples
