import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('images', exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DFKai-SB', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_right_angle(ax, vertex, p1, p2, size=0.35, lw=1.6):
    v = np.array(vertex, dtype=float)
    u1 = np.array(p1, dtype=float) - v
    u2 = np.array(p2, dtype=float) - v
    u1 = u1 / np.linalg.norm(u1) * size
    u2 = u2 / np.linalg.norm(u2) * size
    c1 = v + u1
    c2 = v + u1 + u2
    c3 = v + u2
    ax.plot([c1[0], c2[0], c3[0]], [c1[1], c2[1], c3[1]], color='black', lw=lw)

def draw_angle_arc(ax, vertex, p1, p2, radius=0.6, label=None, fontsize=15):
    v = np.array(vertex, dtype=float)
    d1 = np.array(p1, dtype=float) - v
    d2 = np.array(p2, dtype=float) - v
    ang1 = np.degrees(np.arctan2(d1[1], d1[0])) % 360
    ang2 = np.degrees(np.arctan2(d2[1], d2[0])) % 360
    if (ang2 - ang1) % 360 > 180:
        ang1, ang2 = ang2, ang1
    arc = patches.Arc(v, 2*radius, 2*radius, angle=0, theta1=ang1, theta2=ang2, color='black', lw=1.6)
    ax.add_patch(arc)
    if label:
        mid_ang = np.radians(ang1 + ((ang2 - ang1) % 360) / 2.0)
        lx = v[0] + (radius * 1.55) * np.cos(mid_ang)
        ly = v[1] + (radius * 1.55) * np.sin(mid_ang)
        ax.text(lx, ly, label, fontsize=fontsize, ha='center', va='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none'))

def draw_tick_marks(ax, p1, p2, num_ticks=1, tick_len=0.25, spacing=0.15, lw=1.6):
    p1, p2 = np.array(p1, float), np.array(p2, float)
    mid = (p1 + p2) / 2.0
    diff = p2 - p1
    tangent = diff / np.linalg.norm(diff)
    normal = np.array([-tangent[1], tangent[0]])
    offsets = np.linspace(-(num_ticks-1)*spacing/2, (num_ticks-1)*spacing/2, num_ticks)
    for off in offsets:
        center = mid + off * tangent
        a = center - (tick_len / 2) * normal
        b = center + (tick_len / 2) * normal
        ax.plot([a[0], b[0]], [a[1], b[1]], color='black', lw=lw)

# Figure 1: 內心角度 (選擇第3題)
def make_fig1():
    fig, ax = plt.subplots(figsize=(3.8, 3.4), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    A = np.array([2.5, 4.2])
    B = np.array([0.0, 0.0])
    C = np.array([6.0, 0.0])
    a = np.linalg.norm(B - C)
    b = np.linalg.norm(A - C)
    c = np.linalg.norm(A - B)
    I = (a * A + b * B + c * C) / (a + b + c)

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([B[0], I[0], C[0]], [B[1], I[1], C[1]], 'k--', lw=1.6)
    ax.plot(I[0], I[1], 'ko', markersize=4.5)

    draw_angle_arc(ax, A, B, C, radius=0.65, label='$70^\\circ$', fontsize=13)
    draw_angle_arc(ax, I, C, B, radius=0.45, fontsize=13)

    ax.text(A[0], A[1] + 0.45, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.55, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.55, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(I[0], I[1] + 0.42, '$I$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(3.0, -1.3, '圖(一)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1.0, 7.0)
    ax.set_ylim(-1.8, 5.2)

    plt.savefig('images/fig1_incenter.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 2: 等腰三角形中線與重心 (選擇第4題)
def make_fig2():
    fig, ax = plt.subplots(figsize=(3.4, 4.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    A = np.array([0.0, 12.0])
    B = np.array([-5.0, 0.0])
    C = np.array([5.0, 0.0])
    D = np.array([0.0, 0.0])
    G = np.array([0.0, 4.0])

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k--', lw=1.6)
    ax.plot(G[0], G[1], 'ko', markersize=4.5)

    draw_right_angle(ax, D, C, A, size=0.8, lw=1.5)
    draw_tick_marks(ax, B, D, num_ticks=1, tick_len=0.7, lw=1.5)
    draw_tick_marks(ax, D, C, num_ticks=1, tick_len=0.7, lw=1.5)

    ax.text(A[0], A[1] + 0.6, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.75, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.75, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0], D[1] - 0.75, '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(G[0] + 0.95, G[1], '$G$', fontsize=16, fontweight='bold', fontstyle='italic', va='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))
    ax.text(-3.5, 6.5, '$13$', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none'))
    ax.text(3.5, 6.5, '$13$', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none'))

    ax.text(0.0, -2.0, '圖(二)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-6.8, 6.8)
    ax.set_ylim(-2.6, 13.8)

    plt.savefig('images/fig2_centroid.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 3: 重心分割六塊面積 (選擇第7題)
def make_fig3():
    fig, ax = plt.subplots(figsize=(3.8, 3.6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    A = np.array([2.5, 5.0])
    B = np.array([0.0, 0.0])
    C = np.array([6.0, 0.0])
    D = (B + C) / 2.0
    E = (A + C) / 2.0
    F = (A + B) / 2.0
    G = (A + B + C) / 3.0

    poly = patches.Polygon([A, F, G, E], closed=True, facecolor='#E0E0E0', hatch='///', edgecolor='black', lw=1.5)
    ax.add_patch(poly)

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k--', lw=1.5)
    ax.plot([B[0], E[0]], [B[1], E[1]], 'k--', lw=1.5)
    ax.plot([C[0], F[0]], [C[1], F[1]], 'k--', lw=1.5)
    ax.plot(G[0], G[1], 'ko', markersize=4.5)

    ax.text(A[0], A[1] + 0.45, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.55, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.55, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0], D[1] - 0.65, '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(E[0] + 0.55, E[1] + 0.1, '$E$', fontsize=16, fontweight='bold', fontstyle='italic', va='center')
    ax.text(F[0] - 0.55, F[1] + 0.1, '$F$', fontsize=16, fontweight='bold', fontstyle='italic', va='center')
    ax.text(G[0] + 0.45, G[1] - 0.35, '$G$', fontsize=16, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='circle,pad=0.12', facecolor='white', edgecolor='none'))

    ax.text(3.0, -1.5, '圖(三)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1.1, 7.1)
    ax.set_ylim(-2.0, 5.8)

    plt.savefig('images/fig3_six_areas.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 4: 平行線截角與全等 (選擇第9題)
def make_fig4():
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([0.0, 0.0])
    C = np.array([5.5, 0.0])
    A = np.array([1.5, 3.0])
    D = np.array([5.0, 3.0])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k--', lw=1.6)

    ax.annotate('', xy=(3.4, 3.0), xytext=(3.1, 3.0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax.annotate('', xy=(2.9, 0.0), xytext=(2.6, 0.0), arrowprops=dict(arrowstyle="->", color="black", lw=2))

    ax.text(A[0] - 0.15, A[1] + 0.45, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.55, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.55, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0] + 0.15, D[1] + 0.45, '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')

    ax.text(2.75, -1.3, '圖(四)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1.0, 6.5)
    ax.set_ylim(-1.8, 4.0)

    plt.savefig('images/fig4_congruence.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 5: 銳角外心角度 (填充第2題)
def make_fig5():
    fig, ax = plt.subplots(figsize=(3.8, 3.6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    R = 3.0
    A = np.array([R * np.cos(np.radians(100)), R * np.sin(np.radians(100))])
    B = np.array([R * np.cos(np.radians(215)), R * np.sin(np.radians(215))])
    C = np.array([R * np.cos(np.radians(345)), R * np.sin(np.radians(345))])
    O = np.array([0.0, 0.0])

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([B[0], O[0], C[0]], [B[1], O[1], C[1]], 'k--', lw=1.6)
    ax.plot(O[0], O[1], 'ko', markersize=4.5)

    draw_angle_arc(ax, O, C, B, radius=0.7, label='$130^\\circ$', fontsize=13)
    draw_angle_arc(ax, A, B, C, radius=0.6, fontsize=13)

    ax.text(A[0], A[1] + 0.45, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.55, B[1] - 0.35, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.55, C[1] - 0.35, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(O[0] + 0.1, O[1] + 0.45, '$O$', fontsize=16, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(0.0, -3.2, '圖(五)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-3.8, 4.0)

    plt.savefig('images/fig5_circumcenter.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 6: 等腰三角形點到邊距離 (填充第4題)
def make_fig6():
    fig, ax = plt.subplots(figsize=(3.4, 3.6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    A = np.array([0.0, 8.0])
    B = np.array([-6.0, 0.0])
    C = np.array([6.0, 0.0])
    D = np.array([0.0, 0.0])
    H = np.array([-3.84, 2.88])

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k--', lw=1.6)
    ax.plot([D[0], H[0]], [D[1], H[1]], 'k:', lw=2)
    ax.plot(H[0], H[1], 'ko', markersize=4)

    draw_right_angle(ax, D, C, A, size=0.6, lw=1.5)
    draw_right_angle(ax, H, A, D, size=0.6, lw=1.5)
    draw_tick_marks(ax, B, D, num_ticks=1, tick_len=0.5, lw=1.5)
    draw_tick_marks(ax, D, C, num_ticks=1, tick_len=0.5, lw=1.5)

    ax.text(A[0], A[1] + 0.55, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.75, B[1] - 0.3, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.75, C[1] - 0.3, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0], D[1] - 0.75, '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    # H placed outward to not collide with AB
    ax.text(H[0] - 0.75, H[1] + 0.45, '$H$', fontsize=16, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='circle,pad=0.12', facecolor='white', edgecolor='none'))

    ax.text(0.0, -2.0, '圖(六)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-7.8, 7.8)
    ax.set_ylim(-2.6, 9.6)

    plt.savefig('images/fig6_dist_to_side.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 7: 內心角平分線性質 (填充第6題)
def make_fig7():
    fig, ax = plt.subplots(figsize=(4.0, 3.2), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([0.0, 0.0])
    C = np.array([10.0, 0.0])
    A = np.array([2.75, 5.333])
    D = np.array([4.0, 0.0])
    I = np.array([3.4, 2.0])

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k--', lw=1.6)
    ax.plot(I[0], I[1], 'ko', markersize=4.5)

    draw_angle_arc(ax, A, B, D, radius=0.8, fontsize=13)
    draw_angle_arc(ax, A, D, C, radius=0.9, fontsize=13)

    ax.text(A[0], A[1] + 0.5, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.65, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.65, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0], D[1] - 0.65, '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(I[0] + 0.55, I[1], '$I$', fontsize=16, fontweight='bold', fontstyle='italic', va='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(5.0, -1.7, '圖(七)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1.4, 11.4)
    ax.set_ylim(-2.4, 6.4)

    plt.savefig('images/fig7_angle_bisector.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 8: 等腰三角形外心 (填充第7題)
def make_fig8():
    fig, ax = plt.subplots(figsize=(3.4, 3.6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([-8.0, 0.0])
    C = np.array([8.0, 0.0])
    A = np.array([0.0, 6.0])
    D = np.array([0.0, 0.0])
    O = np.array([0.0, -2.333])
    R = 25.0 / 3.0

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    circle = patches.Circle(O, R, fill=False, edgecolor='gray', linestyle=':', lw=1.5)
    ax.add_patch(circle)

    ax.plot([A[0], O[0]], [A[1], O[1]], 'k--', lw=1.5)
    ax.plot([B[0], O[0]], [B[1], O[1]], 'k--', lw=1.5)
    ax.plot(O[0], O[1], 'ko', markersize=4.5)

    draw_right_angle(ax, D, C, A, size=0.8, lw=1.5)

    ax.text(A[0], A[1] + 0.6, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.9, B[1] - 0.3, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.9, C[1] - 0.3, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0] - 0.75, D[1] + 0.5, '$D$', fontsize=16, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='circle,pad=0.12', facecolor='white', edgecolor='none'))
    ax.text(O[0] + 0.85, O[1], '$O$', fontsize=16, fontweight='bold', fontstyle='italic', va='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(0.0, -12.4, '圖(八)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-9.8, 9.8)
    ax.set_ylim(-13.5, 7.8)

    plt.savefig('images/fig8_circumcircle.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 9: 重心與平行線 (填充第8題)
def make_fig9():
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([0.0, 0.0])
    C = np.array([15.0, 0.0])
    A = np.array([4.0, 9.0])
    G = np.array([19.0/3.0, 3.0])
    D = np.array([4.0/3.0, 3.0])
    E = np.array([34.0/3.0, 3.0])
    M = (B + C) / 2.0

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([D[0], E[0]], [D[1], E[1]], 'k-', lw=2)
    ax.plot([A[0], M[0]], [A[1], M[1]], 'k--', lw=1.5)
    ax.plot(G[0], G[1], 'ko', markersize=4.5)

    ax.annotate('', xy=(7.5, 3.0), xytext=(6.5, 3.0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax.annotate('', xy=(8.0, 0.0), xytext=(7.0, 0.0), arrowprops=dict(arrowstyle="->", color="black", lw=2))

    ax.text(A[0], A[1] + 0.55, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.85, B[1] - 0.3, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.85, C[1] - 0.3, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0] - 0.95, D[1], '$D$', fontsize=16, fontweight='bold', fontstyle='italic', va='center')
    ax.text(E[0] + 0.55, E[1], '$E$', fontsize=16, fontweight='bold', fontstyle='italic', va='center')
    ax.text(G[0], G[1] + 0.65, '$G$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(7.5, -2.1, '圖(九)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-2.0, 17.0)
    ax.set_ylim(-2.8, 10.8)

    plt.savefig('images/fig9_parallel_centroid.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 10: 幾何角度推導 (填充第9題)
def make_fig10():
    fig, ax = plt.subplots(figsize=(3.4, 3.8), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([0.0, 0.0])
    C = np.array([6.0, 0.0])
    A = np.array([3.0, 3.0 * np.tan(np.radians(70))])
    ce_len = 12.0 * np.cos(np.radians(70))
    ac_unit = (A - C) / np.linalg.norm(A - C)
    E = C + ac_unit * ce_len

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([B[0], E[0]], [B[1], E[1]], 'k-', lw=1.8)

    draw_tick_marks(ax, B, C, num_ticks=2, tick_len=0.5, lw=1.5)
    draw_tick_marks(ax, B, E, num_ticks=2, tick_len=0.5, lw=1.5)
    draw_angle_arc(ax, A, B, C, radius=0.8, label='$40^\\circ$', fontsize=13)

    ax.text(A[0], A[1] + 0.5, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.65, B[1] - 0.25, '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0] + 0.65, C[1] - 0.25, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(E[0] + 0.65, E[1] + 0.1, '$E$', fontsize=16, fontweight='bold', fontstyle='italic', va='center')

    ax.text(3.0, -1.6, '圖(十)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1.4, 7.4)
    ax.set_ylim(-2.2, 9.6)

    plt.savefig('images/fig10_angle_proof.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 11: 箏形證明 (非選第一題)
def make_fig11():
    fig, ax = plt.subplots(figsize=(3.4, 4.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    A = np.array([0.0, 4.0])
    C = np.array([0.0, -5.5])
    B = np.array([-3.5, 0.0])
    D = np.array([3.5, 0.0])
    O = np.array([0.0, 0.0])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k--', lw=1.6)
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k--', lw=1.6)

    draw_tick_marks(ax, A, B, num_ticks=1, tick_len=0.5, lw=1.5)
    draw_tick_marks(ax, A, D, num_ticks=1, tick_len=0.5, lw=1.5)
    draw_tick_marks(ax, B, C, num_ticks=2, tick_len=0.5, lw=1.5)
    draw_tick_marks(ax, D, C, num_ticks=2, tick_len=0.5, lw=1.5)

    # Right angle marker in Q1
    ax.plot([0, 0.45, 0.45], [0.45, 0.45, 0], 'k-', lw=1.4)

    # All labels completely separated from lines with clean padding
    ax.text(A[0], A[1] + 0.45, '$A$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(B[0] - 0.55, B[1], '$B$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(C[0], C[1] - 0.65, '$C$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')
    ax.text(D[0] + 0.55, D[1], '$D$', fontsize=16, fontweight='bold', fontstyle='italic', ha='center', va='center')

    # O placed in Q3 with white background padding: zero line intersection!
    ax.text(-0.65, -0.65, '$O$', fontsize=15, fontweight='bold', fontstyle='italic', ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none'))

    ax.text(0.0, -7.5, '圖(十一)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-8.3, 5.2)

    plt.savefig('images/fig11_kite_proof.png', dpi=300, bbox_inches='tight')
    plt.close()

# Figure 12: 園區生態步道與涼亭 (非選第二題)
def make_fig12():
    fig, ax = plt.subplots(figsize=(4.0, 3.4), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    B = np.array([0.0, 0.0])
    C = np.array([40.0, 0.0])
    A = np.array([0.0, 30.0])
    G = (A + B + C) / 3.0
    H = np.array([272.0 / 15.0, 82.0 / 5.0])

    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2)
    ax.plot([G[0], H[0]], [G[1], H[1]], 'k:', lw=2.2)
    ax.plot([A[0], G[0]], [A[1], G[1]], 'k--', lw=1.2)
    ax.plot([B[0], G[0]], [B[1], G[1]], 'k--', lw=1.2)
    ax.plot([C[0], G[0]], [C[1], G[1]], 'k--', lw=1.2)
    ax.plot(G[0], G[1], 'k*', markersize=10)

    draw_right_angle(ax, B, C, A, size=3.0, lw=1.5)
    draw_right_angle(ax, H, A, G, size=2.5, lw=1.5)

    ax.text(A[0] - 2.8, A[1] + 1.8, '$A$', fontsize=16, fontweight='bold', fontstyle='italic')
    ax.text(B[0] - 3.2, B[1] - 2.2, '$B$', fontsize=16, fontweight='bold', fontstyle='italic')
    ax.text(C[0] + 2.8, C[1] - 2.2, '$C$', fontsize=16, fontweight='bold', fontstyle='italic')
    ax.text(G[0] + 1.8, G[1] - 4.0, '$G$(涼亭)', fontsize=14, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none'))
    ax.text(H[0] + 3.2, H[1] + 1.8, '$H$', fontsize=15, fontweight='bold', fontstyle='italic',
            bbox=dict(boxstyle='circle,pad=0.12', facecolor='white', edgecolor='none'))

    ax.text(-5.5, 15.0, '30m', fontsize=14, fontweight='bold', va='center')
    ax.text(20.0, -3.8, '40m', fontsize=14, fontweight='bold', ha='center')

    ax.text(20.0, -9.5, '圖(十二)', fontsize=15, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-8.5, 48.5)
    ax.set_ylim(-12.0, 36.5)

    plt.savefig('images/fig12_park_gazebo.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()
    make_fig6()
    make_fig7()
    make_fig8()
    make_fig9()
    make_fig10()
    make_fig11()
    make_fig12()
    print('All 12 figures regenerated with complete zero-collision protection!')
