import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls

from exam_helpers import (
    set_page_margins, setup_footer_page_number, set_run_font,
    add_jinhe_header, add_section_heading, create_question_p,
    create_options_p, add_question_with_image_top_bottom, safe_save
)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            b = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", 4)}" w:space="0" w:color="{edge_data.get("color", "auto")}"/>')
            tcBorders.append(b)
        else:
            b = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b)
    tcPr.append(tcBorders)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# ==========================================
# 1. 建立試題卷：115上國九數學段三試題.docx
# ==========================================
def build_exam_paper():
    doc = docx.Document()
    set_page_margins(doc, 1.0, 1.0, 1.0, 1.0)
    setup_footer_page_number(doc)
    add_jinhe_header(doc, "第三次段考試題")

    # ---------------- 第一部分：單一選擇題 ----------------
    add_section_heading(doc, "一、單一選擇題（10 題，每題 4 分，共 40 分。請將正確答案依題號填寫於答案卷上）")

    # Q1
    create_question_p(doc, "1. ", "若 a, b 皆為奇數，則下列何者「必為奇數」？", scope_str="(3-1)")
    create_options_p(doc, "(A) a + b　　　(B) a × b　　　(C) a² + b²　　　(D) (a + 1)(b - 1)", space_after=3)

    # Q2
    create_question_p(doc, "2. ", "在直角 △ABC 中，∠C = 90°，線段 AC = 6，線段 BC = 8。若 O 為 △ABC 的外心，則 △ABC 的外接圓半徑為何？", scope_str="(3-2)")
    create_options_p(doc, "(A) 10　　　(B) 24　　　(C) 4　　　(D) 5", space_after=3)

    # Q3 (附圖一，上下型文繞圖)
    add_question_with_image_top_bottom(
        doc, "3. ", 
        "如圖(一)，點 I 為 △ABC 的內心。若 ∠A = 70°，則 ∠BIC 的度數為何？", 
        scope_str="(3-2)", 
        image_path="images/fig1_incenter.png", 
        options_str="(A) 125°　　　(B) 110°　　　(C) 135°　　　(D) 140°", 
        img_width_in=1.65, space_after=3
    )

    # Q4 (附圖二，上下型文繞圖)
    add_question_with_image_top_bottom(
        doc, "4. ", 
        "如圖(二)，△ABC 中，線段 AB = 線段 AC = 13，線段 BC = 10。若 G 為 △ABC 的重心，則線段 AG 的長度為何？", 
        scope_str="(3-2)", 
        image_path="images/fig2_centroid.png", 
        options_str="(A) 4　　　(B) 6　　　(C) 8　　　(D) 12", 
        img_width_in=1.65, space_after=3
    )

    # Q5
    create_question_p(doc, "5. ", "下列哪一個選項可以作為推翻「若 n 為質數，則 n + 2 必為質數」這個敘述的「反例」？", scope_str="(3-1)")
    create_options_p(doc, "(A) n = 3　　　(B) n = 5　　　(C) n = 7　　　(D) n = 9", space_after=3)

    # Q6
    create_question_p(doc, "6. ", "在 △ABC 中，已知 ∠A = 35°，∠B = 45°。則 △ABC 的外心 O 落在何處？", scope_str="(3-2)")
    create_options_p(doc, "(A) △ABC 的內部　　　　　　　　(B) △ABC 的某個頂點上", space_after=1)
    create_options_p(doc, "(C) △ABC 最長邊的中點上　　　　(D) △ABC 的外部", space_after=3)

    # Q7 (附圖三，上下型文繞圖)
    add_question_with_image_top_bottom(
        doc, "7. ", 
        "如圖(三)，G 為 △ABC 的重心，△ABC 的面積為 48。若 D、E、F 分別為線段 BC、AC、AB 的中點，則斜線四邊形 AFGE 的面積為何？", 
        scope_str="(3-2)", 
        image_path="images/fig3_six_areas.png", 
        options_str="(A) 12　　　(B) 16　　　(C) 24　　　(D) 32", 
        img_width_in=1.65, space_after=3
    )

    # Q8
    create_question_p(doc, "8. ", "直角 △ABC 中，兩股長分別為 5 與 12，則其內切圓半徑 r 為何？", scope_str="(3-2)")
    create_options_p(doc, "(A) 2　　　(B) 1　　　(C) 3　　　(D) 6.5", space_after=3)

    # Q9 (附圖四，上下型文繞圖)
    add_question_with_image_top_bottom(
        doc, "9. ", 
        "如圖(四)，四邊形 ABCD 中，已知線段 AD // 線段 BC。小錦想要證明 △ABC ≅ △CDA，他還需要加上下列哪一個條件？", 
        scope_str="(3-1)", 
        image_path="images/fig4_congruence.png", 
        options_str="(A) 線段 AB = 線段 CD　　　(B) 線段 AD = 線段 BC　　　(C) ∠B = ∠D　　　(D) ∠BAC = ∠DCA", 
        img_width_in=1.65, space_after=3
    )

    # Q10
    create_question_p(doc, "10. ", "若正 △ABC 的外接圓半徑為 6，則正 △ABC 的內切圓面積為何？", scope_str="(3-2)")
    create_options_p(doc, "(A) 9π　　　(B) 12π　　　(C) 18π　　　(D) 36π", space_after=4)

    # ---------------- 第二部分：填充題（試題卷無答案格） ----------------
    add_section_heading(doc, "二、填充題（10 格，每格 4 分，共 40 分。請將答案依格號書寫於答案卷對應欄位中，全對才給分）")

    # Fill 1
    create_question_p(doc, "1. ", "在平面直角坐標系中，△ABC 的三頂點坐標分別為 A(-2, 5)、B(4, -3)、C(7, 4)，則 △ABC 的重心 G 之坐標為 ____________。", scope_str="(3-2)", space_after=3)

    # Fill 2 (附圖五)
    add_question_with_image_top_bottom(
        doc, "2. ", 
        "如圖(五)，點 O 為銳角 △ABC 的外心。若 ∠BOC = 130°，則 ∠A = ____________ 度。", 
        scope_str="(3-2)", 
        image_path="images/fig5_circumcenter.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 3
    create_question_p(doc, "3. ", "若 △ABC 的三邊長分別為 7、8、9，其面積為 12√5，則 △ABC 的內切圓半徑為 ____________。", scope_str="(3-2)", space_after=3)

    # Fill 4 (附圖六)
    add_question_with_image_top_bottom(
        doc, "4. ", 
        "如圖(六)，等腰 △ABC 中，線段 AB = 線段 AC = 10，線段 BC = 12。若 D 為線段 BC 的中點，則點 D 到線段 AB 的垂直距離為 ____________。", 
        scope_str="(3-1)", 
        image_path="images/fig6_dist_to_side.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 5
    create_question_p(doc, "5. ", "若直角 △ABC 的兩股長分別為 9 與 12，則其斜邊上的中線長為 ____________。", scope_str="(3-2)", space_after=3)

    # Fill 6 (附圖七)
    add_question_with_image_top_bottom(
        doc, "6. ", 
        "如圖(七)，在 △ABC 中，I 為內心，線段 AI 的延長線交線段 BC 於 D 點。已知線段 AB = 6，線段 AC = 9，線段 BC = 10，則線段 BD 的長度為 ____________。", 
        scope_str="(3-2)", 
        image_path="images/fig7_angle_bisector.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 7 (附圖八)
    add_question_with_image_top_bottom(
        doc, "7. ", 
        "如圖(八)，在等腰 △ABC 中，線段 AB = 線段 AC = 10，線段 BC = 16。則 △ABC 的外接圓半徑為 ____________。", 
        scope_str="(3-2)", 
        image_path="images/fig8_circumcircle.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 8 (附圖九)
    add_question_with_image_top_bottom(
        doc, "8. ", 
        "如圖(九)，G 為 △ABC 的重心。過 G 點作直線平行於線段 BC，分別交線段 AB、AC 於 D、E 兩點。若線段 BC = 15，則線段 DE 的長度為 ____________。", 
        scope_str="(3-2)", 
        image_path="images/fig9_parallel_centroid.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 9 (附圖十)
    add_question_with_image_top_bottom(
        doc, "9. ", 
        "如圖(十)，已知等腰 △ABC 中，線段 AB = 線段 AC，∠A = 40°。若點 E 在線段 AC 上使得線段 BE = 線段 BC，則 ∠CBE = ____________ 度。", 
        scope_str="(3-1)", 
        image_path="images/fig10_angle_proof.png", 
        img_width_in=1.65, space_after=3
    )

    # Fill 10
    create_question_p(doc, "10. ", "在直角 △ABC 中，∠C = 90°，兩股長線段 AC = 9，線段 BC = 12。若 O 為 △ABC 的外心，G 為 △ABC 的重心，則線段 OG 的長度為 ____________。", scope_str="(3-2)", space_after=4)

    # ---------------- 第三部分：非選擇題（試題卷無作答方框） ----------------
    add_section_heading(doc, "三、非選擇題（2 題，每題 10 分，共 20 分。請在答案卷規定之欄位內書寫完整推導與計算過程，無推導過程不予計分）")

    # Non-choice 1 (附圖十一)
    create_question_p(doc, "1. ", "如圖(十一)，四邊形 ABCD 中，線段 AB = 線段 AD，線段 CB = 線段 CD（箏形）。對角線線段 AC 與線段 BD 相交於 O 點。", scope_str="(3-1)", space_after=2)
    p_img11 = doc.add_paragraph()
    p_img11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img11.paragraph_format.left_indent = Pt(0)
    p_img11.paragraph_format.space_before = Pt(2)
    p_img11.paragraph_format.space_after = Pt(2)
    p_img11.add_run().add_picture("images/fig11_kite_proof.png", width=Inches(1.55))
    
    p_n1_sub1 = doc.add_paragraph()
    p_n1_sub1.paragraph_format.left_indent = Inches(0.28)
    p_n1_sub1.paragraph_format.space_before = Pt(0)
    p_n1_sub1.paragraph_format.space_after = Pt(2)
    r_n1_1 = p_n1_sub1.add_run("(1) 請證明：△ABC ≅ △ADC。（5 分）")
    set_run_font(r_n1_1, font_name="標楷體", font_size=11)

    p_n1_sub2 = doc.add_paragraph()
    p_n1_sub2.paragraph_format.left_indent = Inches(0.28)
    p_n1_sub2.paragraph_format.space_before = Pt(0)
    p_n1_sub2.paragraph_format.space_after = Pt(4)
    r_n1_2 = p_n1_sub2.add_run("(2) 請進一步證明：線段 AC ⊥ 線段 BD，且線段 AC 平分線段 BD（即線段 AC 為線段 BD 的垂直平分線）。（5 分）")
    set_run_font(r_n1_2, font_name="標楷體", font_size=11)

    # Non-choice 2 (附圖十二)
    create_question_p(doc, "2. ", "「新北綠美化園區」規劃在如圖(十二)的直角三角形空地 △ABC 內設置生態步道與休憩涼亭。已知 ∠B = 90°，線段 AB = 30 公尺，線段 BC = 40 公尺。工程處規劃將休憩涼亭設置在該空地的重心 G 處，並自 G 點開闢三條最短步道分別垂直通往三邊線段 AB、BC、AC。", scope_str="(3-2)", space_after=2)
    p_img12 = doc.add_paragraph()
    p_img12.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img12.paragraph_format.left_indent = Pt(0)
    p_img12.paragraph_format.space_before = Pt(2)
    p_img12.paragraph_format.space_after = Pt(2)
    p_img12.add_run().add_picture("images/fig12_park_gazebo.png", width=Inches(1.75))

    p_n2_sub1 = doc.add_paragraph()
    p_n2_sub1.paragraph_format.left_indent = Inches(0.28)
    p_n2_sub1.paragraph_format.space_before = Pt(0)
    p_n2_sub1.paragraph_format.space_after = Pt(2)
    r_n2_1 = p_n2_sub1.add_run("(1) 請計算出斜邊線段 AC 的長度，以及 △ABC 的總面積。（4 分）")
    set_run_font(r_n2_1, font_name="標楷體", font_size=11)

    p_n2_sub2 = doc.add_paragraph()
    p_n2_sub2.paragraph_format.left_indent = Inches(0.28)
    p_n2_sub2.paragraph_format.space_before = Pt(0)
    p_n2_sub2.paragraph_format.space_after = Pt(4)
    r_n2_2 = p_n2_sub2.add_run("(2) 若工程處需計算涼亭 G 到最長步道邊（即斜邊線段 AC）的垂直距離，請利用三角形重心分割面積等性質，求出此垂直距離為多少公尺？（6 分）")
    set_run_font(r_n2_2, font_name="標楷體", font_size=11)

    filename = "115上國九數學段三試題.docx"
    saved = safe_save(doc, filename)
    return saved

# ==========================================
# 2. 建立獨立答案卷：115上國九數學段三答案卷.docx
# ==========================================
def build_answer_sheet():
    doc = docx.Document()
    set_page_margins(doc, 1.0, 1.0, 1.0, 1.0)
    setup_footer_page_number(doc)

    # 抬頭、命題範圍與學生資訊、警語（比照解析卷格式）
    add_jinhe_header(doc, "第三次段考 答案卷")

    # ◆ 第一部分：單一選擇題（每題 4 分，共 40 分）
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run("◆ 第一部分：單一選擇題（每題 4 分，共 40 分）")
    set_run_font(r_mc, font_name="標楷體", font_size=10.5, bold=True)

    t_mc = doc.add_table(rows=2, cols=10)
    t_mc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i in range(10):
        c0 = t_mc.cell(0, i)
        c1 = t_mc.cell(1, i)
        c0.width = Inches(0.748)
        c1.width = Inches(0.748)
        set_cell_border(c0, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        set_cell_border(c1, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_k = p0.add_run(str(i + 1))
        set_run_font(r_k, font_name="Times New Roman", font_size=10, bold=True)
        set_cell_margins(c0, top=20, bottom=20, left=20, right=20)
        set_cell_margins(c1, top=100, bottom=100, left=20, right=20)

    # ◆ 第二部分：填充題（每格 4 分，共 40 分）
    p_f = doc.add_paragraph()
    p_f.paragraph_format.space_before = Pt(2)
    p_f.paragraph_format.space_after = Pt(1)
    r_f = p_f.add_run("◆ 第二部分：填充題（每格 4 分，共 40 分）")
    set_run_font(r_f, font_name="標楷體", font_size=10.5, bold=True)

    t_f = doc.add_table(rows=4, cols=5)
    t_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    fill_indices = [
        ["1", "2", "3", "4", "5"],
        ["", "", "", "", ""],
        ["6", "7", "8", "9", "10"],
        ["", "", "", "", ""]
    ]
    for r_idx in range(4):
        for c_idx in range(5):
            cell = t_f.cell(r_idx, c_idx)
            cell.width = Inches(1.496)
            set_cell_border(cell, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if r_idx in (0, 2):
                set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
                r = p.add_run(fill_indices[r_idx][c_idx])
                set_run_font(r, font_name="Times New Roman", font_size=10, bold=True)
            else:
                set_cell_margins(cell, top=110, bottom=110, left=40, right=40)

    # ◆ 第三部分：非選擇題（每題 10 分，共 20 分。請寫出完整推導與計算過程）
    p_n = doc.add_paragraph()
    p_n.paragraph_format.space_before = Pt(2)
    p_n.paragraph_format.space_after = Pt(1)
    r_n = p_n.add_run("◆ 第三部分：非選擇題（每題 10 分，共 20 分。請寫出完整推導與計算過程）")
    set_run_font(r_n, font_name="標楷體", font_size=10.5, bold=True)

    t_n = doc.add_table(rows=2, cols=2)
    t_n.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in t_n.columns:
        c.width = Inches(3.74)

    for row in t_n.rows:
        for c in row.cells:
            set_cell_border(c, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))

    p_n1 = t_n.cell(0, 0).paragraphs[0]
    p_n1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_n1.add_run("非選第 1 題（箏形垂直平分證明，共 10 分）")
    set_run_font(r1, font_name="標楷體", font_size=10, bold=True)
    set_cell_margins(t_n.cell(0, 0), top=25, bottom=25, left=60, right=60)

    p_n2 = t_n.cell(0, 1).paragraphs[0]
    p_n2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p_n2.add_run("非選第 2 題（園區涼亭步道距離計算，共 10 分）")
    set_run_font(r2, font_name="標楷體", font_size=10, bold=True)
    set_cell_margins(t_n.cell(0, 1), top=25, bottom=25, left=60, right=60)

    set_cell_margins(t_n.cell(1, 0), top=35, bottom=35, left=60, right=60)
    set_cell_margins(t_n.cell(1, 1), top=35, bottom=35, left=60, right=60)
    for _ in range(11):
        t_n.cell(1, 0).add_paragraph()
        t_n.cell(1, 1).add_paragraph()

    filename = "115上國九數學段三答案卷.docx"
    saved = safe_save(doc, filename)
    return saved

# ==========================================
# 3. 建立答案與詳細解析卷：115上國九數學段三答案與詳解.docx
# ==========================================
def build_solution_paper():
    doc = docx.Document()
    set_page_margins(doc, 1.0, 1.0, 1.0, 1.0)
    setup_footer_page_number(doc)
    add_jinhe_header(doc, "第三次段考 答案與詳細解析卷")

    add_section_heading(doc, "【標準答案速查表】")

    # 選擇題速查
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.left_indent = Pt(0)
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run("◆ 第一部分：單一選擇題（每題 4 分，共 40 分）")
    set_run_font(r_mc, font_name="標楷體", font_size=10.5, bold=True)

    t_mc = doc.add_table(rows=2, cols=10)
    t_mc.alignment = WD_TABLE_ALIGNMENT.CENTER
    mc_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    mc_ans = ["B", "D", "A", "C", "C", "D", "B", "A", "B", "A"]
    for i in range(10):
        c0 = t_mc.cell(0, i)
        c1 = t_mc.cell(1, i)
        c0.width = Inches(0.74)
        c1.width = Inches(0.74)
        set_cell_border(c0, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
        set_cell_border(c1, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_k = p0.add_run(mc_keys[i])
        set_run_font(r_k, font_name="Times New Roman", font_size=10, bold=True)
        r_a = p1.add_run(mc_ans[i])
        set_run_font(r_a, font_name="Times New Roman", font_size=11, bold=True, color=RGBColor(180, 0, 0))

    # 填充題速查
    p_f = doc.add_paragraph()
    p_f.paragraph_format.left_indent = Pt(0)
    p_f.paragraph_format.space_before = Pt(4)
    p_f.paragraph_format.space_after = Pt(2)
    r_f = p_f.add_run("◆ 第二部分：填充題（每格 4 分，共 40 分）")
    set_run_font(r_f, font_name="標楷體", font_size=10.5, bold=True)

    t_f = doc.add_table(rows=4, cols=5)
    t_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    fill_keys = [
        ["1", "2", "3", "4", "5"],
        ["(3, 2)", "65", "√5", "24/5 (或 4.8)", "15/2 (或 7.5)"],
        ["6", "7", "8", "9", "10"],
        ["4", "25/3", "10", "40", "5/2 (或 2.5)"]
    ]
    for r_idx in range(4):
        for c_idx in range(5):
            cell = t_f.cell(r_idx, c_idx)
            cell.width = Inches(1.48)
            set_cell_border(cell, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            val = fill_keys[r_idx][c_idx]
            if r_idx in (0, 2):
                r = p.add_run(val)
                set_run_font(r, font_name="Times New Roman", font_size=10, bold=True)
            else:
                r = p.add_run(val)
                set_run_font(r, font_name="Times New Roman", font_size=10.5, bold=True, color=RGBColor(180, 0, 0))

    # 非選題速查
    p_n = doc.add_paragraph()
    p_n.paragraph_format.left_indent = Pt(0)
    p_n.paragraph_format.space_before = Pt(4)
    p_n.paragraph_format.space_after = Pt(2)
    r_n = p_n.add_run("◆ 第三部分：非選擇題（每題 10 分，共 20 分）")
    set_run_font(r_n, font_name="標楷體", font_size=10.5, bold=True)

    t_n = doc.add_table(rows=2, cols=2)
    t_n.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_n.cell(0, 0).width = Inches(3.7)
    t_n.cell(0, 1).width = Inches(3.7)
    t_n.cell(1, 0).width = Inches(3.7)
    t_n.cell(1, 1).width = Inches(3.7)
    for row in t_n.rows:
        for c in row.cells:
            set_cell_border(c, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))

    p_n1_h = t_n.cell(0, 0).paragraphs[0]
    p_n1_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_n1_h.add_run("非選第 1 題（箏形垂直平分證明）")
    set_run_font(r, font_name="標楷體", font_size=10, bold=True)

    p_n2_h = t_n.cell(0, 1).paragraphs[0]
    p_n2_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_n2_h.add_run("非選第 2 題（園區涼亭步道距離）")
    set_run_font(r, font_name="標楷體", font_size=10, bold=True)

    p_n1_a = t_n.cell(1, 0).paragraphs[0]
    r = p_n1_a.add_run("(1) 利用 SSS 證明 △ABC ≅ △ADC\n(2) 利用對應角相等由 SAS 得垂直且平分")
    set_run_font(r, font_name="標楷體", font_size=9.5, color=RGBColor(180, 0, 0))

    p_n2_a = t_n.cell(1, 1).paragraphs[0]
    r = p_n2_a.add_run("(1) 斜邊 AC = 50 公尺，面積 = 600 平方公尺\n(2) 涼亭到斜邊垂直距離 = 8 公尺")
    set_run_font(r, font_name="標楷體", font_size=9.5, color=RGBColor(180, 0, 0))

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 逐題詳解（導入前述驗證內容）
    from solutions_data import solutions
    for title, ans_badge, meta, body in solutions:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.left_indent = Pt(0)
        p_t.paragraph_format.space_before = Pt(4)
        p_t.paragraph_format.space_after = Pt(1)
        r_t = p_t.add_run(f"【{title}】 正確答案：{ans_badge}")
        set_run_font(r_t, font_name="標楷體", font_size=11, bold=True, color=RGBColor(0, 51, 102))

        p_m = doc.add_paragraph()
        p_m.paragraph_format.left_indent = Pt(0)
        p_m.paragraph_format.space_before = Pt(0)
        p_m.paragraph_format.space_after = Pt(1)
        r_m = p_m.add_run(meta)
        set_run_font(r_m, font_name="Times New Roman", font_size=9.5, italic=True, color=RGBColor(100, 100, 100))

        p_b = doc.add_paragraph()
        p_b.paragraph_format.left_indent = Pt(0)
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(4)
        p_b.paragraph_format.line_spacing = 1.15
        r_b = p_b.add_run(body)
        set_run_font(r_b, font_name="標楷體", font_size=10.5)

    filename = "115上國九數學段三答案與詳解.docx"
    saved = safe_save(doc, filename)
    return saved

# ==========================================
# 4. 建立命題審題檢核表：115上國九數學段三命題審題檢核表.docx
# ==========================================
def build_specification_table():
    doc = docx.Document()
    set_page_margins(doc, 1.0, 1.0, 1.0, 1.0)
    setup_footer_page_number(doc)
    add_jinhe_header(doc, "第三次段考 命題審題雙向細目檢核表")

    add_section_heading(doc, "一、 108 數學課綱「學習內容 × 認知層次」雙向細目分析表")
    t1 = doc.add_table(rows=5, cols=7)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["章節單元與學習內容條目", "認識 (R)", "理解 (U)", "熟練 (F)", "應用與解題 (A)", "題數小計", "配分比重"]
    widths = [Inches(2.2), Inches(0.8), Inches(0.8), Inches(0.8), Inches(1.1), Inches(0.8), Inches(0.9)]
    
    matrix_data = [
        ["3-1 幾何推理與證明 (S-9-11)", "選1, 選5 (8分)", "選9, 填9 (8分)", "填4 (4分)", "非選1 (10分)", "6 題", "30 分 (30%)"],
        ["3-2 三角形的外心 (S-9-8)", "選6 (4分)", "選2, 填2 (8分)", "填5, 填7 (8分)", "填10 (4分)", "6 題", "24 分 (24%)"],
        ["3-2 三角形的內心 (S-9-8)", "-", "選3, 選8 (8分)", "填3, 填6 (8分)", "-", "4 題", "16 分 (16%)"],
        ["3-2 三角形的重心 (S-9-8)", "-", "選4, 選7 (8分)", "選10, 填1 (8分)", "填8, 非選2 (14分)", "6 題", "30 分 (30%)"],
    ]

    for c_idx, h in enumerate(headers):
        cell = t1.cell(0, c_idx)
        cell.width = widths[c_idx]
        set_cell_border(cell, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        set_run_font(r, font_name="標楷體", font_size=10, bold=True)

    for r_idx, row_vals in enumerate(matrix_data):
        for c_idx, val in enumerate(row_vals):
            cell = t1.cell(r_idx + 1, c_idx)
            cell.width = widths[c_idx]
            set_cell_border(cell, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            set_run_font(r, font_name="標楷體", font_size=9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_section_heading(doc, "二、 108 課綱核心素養面向與 PISA 數學思維歷程檢核")
    t2 = doc.add_table(rows=5, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_headers = ["PISA 數學思維歷程", "涵蓋試題題號", "核心素養指標", "命題意涵與檢核要點"]
    t2_widths = [Inches(1.8), Inches(1.8), Inches(1.2), Inches(2.6)]
    t2_data = [
        ["M1 數學推論 (Reasoning)", "選1, 選5, 選9, 填9, 非選1", "數-J-A1, 數-J-C1", "檢驗演繹推理、奇偶代數性質、反例舉證與幾何全等證明。"],
        ["M2 形成問題 (Formulate)", "非選2", "數-J-A3, 數-J-B1", "將真實綠美化園區涼亭工程轉化為直角坐標三角形與重心面積模型。"],
        ["M3 運用程序 (Employ)", "選2, 選3, 選4, 選7, 選8, 填1~7, 填10", "數-J-A2, 數-J-B1", "熟練外心、內心、重心之坐標公式、內切圓半徑與畢氏定理代數程序。"],
        ["M4 詮釋評鑑 (Interpret)", "選6, 選10, 填8, 非選2", "數-J-A3, 數-J-B3", "評估鈍角外心位置合理性、重心平行線比例線段及工程步道距離精確值。"]
    ]
    for c_idx, h in enumerate(t2_headers):
        cell = t2.cell(0, c_idx)
        cell.width = t2_widths[c_idx]
        set_cell_border(cell, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        set_run_font(r, font_name="標楷體", font_size=10, bold=True)
    for r_idx, row_vals in enumerate(t2_data):
        for c_idx, val in enumerate(row_vals):
            cell = t2.cell(r_idx + 1, c_idx)
            cell.width = t2_widths[c_idx]
            set_cell_border(cell, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 3 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            set_run_font(r, font_name="標楷體", font_size=9.5)

    doc.add_page_break()

    add_section_heading(doc, "三、 108 課綱九年級數學科「嚴格防超綱紅線清單」檢核表")
    t3 = doc.add_table(rows=6, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ["法定課綱禁區（108 課綱備註欄明確規範）", "檢核狀態", "本試卷落實說明"]
    t3_widths = [Inches(3.2), Inches(1.0), Inches(3.2)]
    t3_data = [
        ["二次函數一般式配方法求極值（已移至 10 年級 F-10-1）", "☑ 通過", "全卷未涉及二次函數配方法，聚焦於幾何推理與三心。"],
        ["舊課綱圓冪定理、公切線長公式、弦切角定理（已刪除）", "☑ 通過", "無涉及切割線、內外冪或公切線長，純粹評量內外心圓幾何。"],
        ["非特殊角三角比或高次三角恆等式（限 30°/45°/60°）", "☑ 通過", "無非特殊角之三角比，長度計算皆使用畢氏定理與相似形。"],
        ["多邊形外心/重心之複雜解析幾何運算（限三角形三心）", "☑ 通過", "嚴格限定於三角形之三心性質，不跨入高維幾何或圓錐曲線。"],
        ["超越本章節之空間立體向量外積（已移至高中 11A 軌）", "☑ 通過", "空間幾何純粹未涉及，百分之百鎖定平面幾何證明與三心。"]
    ]
    for c_idx, h in enumerate(t3_headers):
        cell = t3.cell(0, c_idx)
        cell.width = t3_widths[c_idx]
        set_cell_border(cell, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        set_run_font(r, font_name="標楷體", font_size=10, bold=True)
    for r_idx, row_vals in enumerate(t3_data):
        for c_idx, val in enumerate(row_vals):
            cell = t3.cell(r_idx + 1, c_idx)
            cell.width = t3_widths[c_idx]
            set_cell_border(cell, top=dict(val='single', sz=4), bottom=dict(val='single', sz=4), left=dict(val='single', sz=4), right=dict(val='single', sz=4))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            set_run_font(r, font_name="標楷體", font_size=9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_section_heading(doc, "四、 錦和高中試務組排版與審題簽章檢核")
    t4 = doc.add_table(rows=2, cols=4)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_headers = ["命題教師簽章", "審題教師簽章", "領域召集人簽章", "教務處教學組核定"]
    for c_idx, h in enumerate(t4_headers):
        c0 = t4.cell(0, c_idx)
        c1 = t4.cell(1, c_idx)
        c0.width = Inches(1.85)
        c1.width = Inches(1.85)
        set_cell_border(c0, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        set_cell_border(c1, top=dict(val='single', sz=6), bottom=dict(val='single', sz=6), left=dict(val='single', sz=6), right=dict(val='single', sz=6))
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(h)
        set_run_font(r0, font_name="標楷體", font_size=10, bold=True)
        set_cell_margins(c1, top=300, bottom=300, left=100, right=100)

    filename = "115上國九數學段三命題審題檢核表.docx"
    saved = safe_save(doc, filename)
    return saved

if __name__ == '__main__':
    f1 = build_exam_paper()
    f2 = build_answer_sheet()
    f3 = build_solution_paper()
    f4 = build_specification_table()
    print("All 4 files created successfully!")
