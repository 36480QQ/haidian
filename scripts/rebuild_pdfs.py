import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

plt.rcParams['font.sans-serif'] = ['Songti SC', 'PingFang SC', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

sub = Path('/Users/yuanyi/MyProject/vibeP/haidian/submissions/YuanYii/jingzhang-ai-nexus')
assets = sub / 'assets/figures'
out_dir = sub / 'drawings'
out_dir.mkdir(exist_ok=True)

WARNING_ZH = "注意：图件基于临时约束边界（provisional constraint）生成，不构成法定控规红线。所有几何、指标与数据均为概念建议，须待官方红线发布后由专业部门核验重算。"
WARNING_EN = "WARNING: Figures are based on provisional boundaries and do not constitute official redlines. All geometries and metrics are conceptual and must be re-verified post official release."

IMAGES = [
    ("site-overview", "总体区位与设计范围"),
    ("land-use-structure", "总体用地结构与功能分区"),
    ("key-areas", "三处重点区域详细设计指引"),
    ("mobility-bluegreen", "交通慢行与蓝绿公共空间复合系统"),
    ("metrics-evidence", "指标证据链验证面板")
]

def create_pdf(filename, lang='zh'):
    # A3 size in inches: 11.7 x 16.5, landscape is 16.5 x 11.7
    # For a multi-page PDF, we use PdfPages
    from matplotlib.backends.backend_pdf import PdfPages
    
    warning = WARNING_EN if lang == 'en' else WARNING_ZH
    suffix = ".en.png" if lang == 'en' else ".png"
    pdf_path = out_dir / filename
    
    with PdfPages(pdf_path) as pdf:
        # Cover Page
        fig = plt.figure(figsize=(16.5, 11.7))
        fig.text(0.5, 0.6, "百年京张AI创新带城市设计" if lang == 'zh' else "Centennial Jing-Zhang AI Innovation Belt Urban Design", 
                 ha='center', va='center', fontsize=36, fontweight='bold')
        fig.text(0.5, 0.5, "概念方案图册" if lang == 'zh' else "Conceptual Design Booklet", 
                 ha='center', va='center', fontsize=24)
        fig.text(0.5, 0.4, warning, ha='center', va='center', fontsize=12, color='red', bbox=dict(facecolor='yellow', alpha=0.3))
        pdf.savefig(fig)
        plt.close(fig)
        
        # Content Pages
        for img_name, title_zh in IMAGES:
            img_path = assets / f"{img_name}{suffix}"
            if not img_path.exists():
                img_path = assets / f"{img_name}.png" # fallback
            
            fig = plt.figure(figsize=(16.5, 11.7))
            if img_path.exists():
                img = mpimg.imread(str(img_path))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.75])
                ax.imshow(img)
                ax.axis('off')
            
            title = title_zh if lang == 'zh' else img_name.replace('-', ' ').title()
            fig.text(0.5, 0.9, title, ha='center', va='center', fontsize=24, fontweight='bold')
            fig.text(0.5, 0.05, warning, ha='center', va='center', fontsize=12, color='red')
            pdf.savefig(fig)
            plt.close(fig)

    print(f"Saved {pdf_path}")

# Create A3 booklets
create_pdf("a3-booklet.pdf", "zh")
create_pdf("a3-booklet.en.pdf", "en")

# Create A0 boards (Just slightly different size/layout, but we can reuse for now to ensure compliance)
# A0 size in inches: 33.1 x 46.8
def create_a0(filename, lang='zh'):
    warning = WARNING_EN if lang == 'en' else WARNING_ZH
    suffix = ".en.png" if lang == 'en' else ".png"
    pdf_path = out_dir / filename
    
    fig = plt.figure(figsize=(33.1, 46.8))
    fig.text(0.5, 0.95, "百年京张AI创新带城市设计展板" if lang == 'zh' else "Jing-Zhang AI Innovation Belt Boards", 
             ha='center', va='center', fontsize=48, fontweight='bold')
    fig.text(0.5, 0.92, warning, ha='center', va='center', fontsize=24, color='red', bbox=dict(facecolor='yellow', alpha=0.3))
    
    for i, (img_name, _) in enumerate(IMAGES):
        img_path = assets / f"{img_name}{suffix}"
        if not img_path.exists():
            img_path = assets / f"{img_name}.png"
            
        if img_path.exists():
            img = mpimg.imread(str(img_path))
            # Grid layout 3x2
            row = i // 2
            col = i % 2
            ax = fig.add_axes([0.05 + col*0.45, 0.65 - row*0.28, 0.4, 0.25])
            ax.imshow(img)
            ax.axis('off')

    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig)
    plt.close(fig)
    print(f"Saved {pdf_path}")

create_a0("a0-boards.pdf", "zh")
create_a0("a0-boards.en.pdf", "en")

# Ensure valid PDF signatures by matplotlib
