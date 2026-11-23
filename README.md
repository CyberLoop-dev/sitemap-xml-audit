<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:101b2a,100:0284c7&height=170&section=header&text=sitemap-xml-audit&fontColor=ffffff&fontSize=40)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&center=true&vCenter=true&width=620&lines=Validate+local+XML+sitemaps;Find+bad+URLs+and+duplicate+entries" alt="Typing title"/>

[![License](https://img.shields.io/github/license/CyberLoop-dev/sitemap-xml-audit)](LICENSE)
![Language](https://img.shields.io/github/languages/top/CyberLoop-dev/sitemap-xml-audit)
[![Stars](https://img.shields.io/github/stars/CyberLoop-dev/sitemap-xml-audit?style=social)](https://github.com/CyberLoop-dev/sitemap-xml-audit/stargazers)
![Last commit](https://img.shields.io/github/last-commit/CyberLoop-dev/sitemap-xml-audit)

<img src="assets/mark.svg" width="520" alt="Sitemap structure illustration"/>

</div>

## 🧭 Overview
A dependency-free Python CLI for checking local XML sitemap files and sitemap indexes. It validates entry structure, absolute HTTP(S) locations, duplicate locations, and optional `lastmod` values. It does not fetch URLs.

## ✨ Features
- 🗺️ Supports `urlset` and `sitemapindex` roots, including namespaced XML.
- 🔗 Checks absolute HTTP(S) `loc` values.
- ♻️ Finds duplicate locations.
- 🕒 Validates ISO date and date-time `lastmod` values.
- 📦 Provides text and JSON reports.

## 🖥️ Demo
The repository includes `sample-sitemap.xml`; no hosted demo is configured.

## 🚀 Quick Start
```bash
python main.py
python main.py path/to/sitemap.xml
python main.py path/to/sitemap.xml --json
python -m unittest discover -s tests
```

## 🧰 Tech Stack
- Python 3.10+
- Standard library: `xml.etree.ElementTree`, `argparse`, `urllib.parse`

## 🗂️ Folder Structure
```text
.
├── assets/mark.svg
├── tests/test_sitemap.py
├── sample-sitemap.xml
├── main.py
├── requirements.txt
└── README.md
```

## 🗺️ Roadmap
- [ ] Add optional sitemap-index file discovery without network access.
- [ ] Export CSV summaries.
- [ ] Add configurable organization-specific limits.

## 🤝 Contributing
Include a small XML fixture and the expected finding for every new validation rule.

## 📄 License
MIT. See [LICENSE](LICENSE).

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:0284c7,100:101b2a&height=100&section=footer)

</div>
