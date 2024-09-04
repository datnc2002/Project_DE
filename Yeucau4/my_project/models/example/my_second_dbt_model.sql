{{config(materialized='table')}}

SELECT
    DATE_FORMAT(STR_TO_DATE(Ngay_hach_toan, '%m/%d/%Y %H:%i'), '%Y-%m') AS thang,
    nv.nhan_vien_ban AS Nhan_vien,
    nv.ma_nhan_vien_ban AS ma_nhan_vien_ban,
    SUM(dlh.doanh_thu) AS Tong_doanh_thu
FROM
    bai_test.du_lieu_ban_hang dlh
JOIN
    bai_test.nhan_vien nv ON dlh.ma_nhan_vien_ban = nv.ma_nhan_vien_ban
GROUP BY
    DATE_FORMAT(STR_TO_DATE(Ngay_hach_toan, '%m/%d/%Y %H:%i'), '%Y-%m'),
    nv.nhan_vien_ban,
    nv.ma_nhan_vien_ban
ORDER BY
    thang,
    nhan_vien
