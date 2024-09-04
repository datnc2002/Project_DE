{{config(materialized='table')}}

SELECT
    DATE_FORMAT(STR_TO_DATE(Ngay_hach_toan, '%m/%d/%Y %H:%i'), '%Y-%m') AS Thang,
    cn.Ten_chi_nhanh AS Chi_nhanh,
    SUM(dlh.Doanh_thu) AS Tong_doanh_thu
FROM
    bai_test.du_lieu_ban_hang dlh
JOIN
    bai_test.chi_nhanh cn ON dlh.chi_nhanh = cn.ma_chi_nhanh
GROUP BY
    DATE_FORMAT(STR_TO_DATE(Ngay_hach_toan, '%m/%d/%Y %H:%i'), '%Y-%m'),
    cn.Ten_chi_nhanh
ORDER BY
    Thang,
    Chi_nhanh