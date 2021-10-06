USE database_time_engenharia_de_dados;

SELECT
	V.ID_PESSOA,
    V.VL_VENDA,
    T.DT_REF,
    T.NU_ANO,
    P.NM_PESSOA,
    L.DS_UF
FROM
    f.Vendas V
        LEFT JOIN
    d_Tempo T ON V.ID_TEMPO = T.ID_TEMPO
        LEFT JOIN
    d_Loja L ON V.ID_LOJA = L.ID_LOJA
        LEFT JOIN
    d_Pessoa P ON V.ID_PESSOA = P.ID_PESSOA
WHERE
    T.NU_MES = 1 AND T.NU_ANO = 2020
        AND LS.DF_UF = 'CE';
