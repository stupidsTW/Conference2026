import os
import glob
import re

def get_title_from_html(html_path):
    """嘗試從 HTML 檔案中讀取 <title> 或第一個 <h1> 作為文章標題"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(2000) # 讀取前 2000 個字元加速
            
            # 尋找 <title>...</title>
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                if title:
                    return title
            
            # 若無 title，尋找第一個 <h1>...</h1>
            h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            if h1_match:
                # 濾除可能的 html 標籤
                clean_h1 = re.sub(r'<.*?>', '', h1_match.group(1)).strip()
                if clean_h1:
                    return clean_h1
    except Exception as e:
        print(f"讀取標題失敗 {html_path}: {e}")
    
    # 若都找不到則回傳檔名作為預設標題
    return os.path.splitext(os.path.basename(html_path))[0]

def main():
    # 尋找資料夾下所有的 .html 檔案（排除 index.html 自身）
    html_files = [f for f in glob.glob("*.html") if os.path.basename(f).lower() != "index.html"]
    
    papers = []
    for html_file in sorted(html_files):
        base_name = os.path.splitext(html_file)[0]
        title = get_title_from_html(html_file)
        media_dir = f"{base_name}_media"
        has_media = os.path.exists(media_dir)
        
        papers.append({
            "filename": html_file,
            "title": title,
            "base_name": base_name,
            "has_media": has_media
        })
    
    print(f"找到 {len(papers)} 篇論文 HTML 檔案。")

    # 產生 index.html 內容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研討會論文集</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>研討會論文集</h1>
            <p class="subtitle">Seminar Proceedings & Paper Repository</p>
        </header>

        <main>
            <section class="paper-list">
                <h2>已收錄論文列表</h2>
"""

    if not papers:
        html_content += """                <p class="no-papers">目前尚無收錄的論文，請先執行轉換程式。</p>
"""
    else:
        html_content += """                <ul class="papers-grid">
"""
        for p in papers:
            html_content += f"""                    <li class="paper-card">
                        <div class="paper-info">
                            <h3 class="paper-title"><a href="{p['filename']}">{p['title']}</a></h3>
                            <span class="paper-file-id">檔案代號：<code>{p['base_name']}</code></span>
                        </div>
                        <div class="paper-actions">
                            <a href="{p['filename']}" class="btn-read" target="_blank">閱讀內文</a>
                        </div>
                    </li>
"""
        html_content += """                </ul>
"""

    html_content += """            </section>
        </main>

        <footer>
            <p>&copy; 2026 Seminar Committee. Hosted on GitHub Pages.</p>
        </footer>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("index.html 產生成功！")

if __name__ == "__main__":
    main()
