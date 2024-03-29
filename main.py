import requests
import datetime
import shutil
import subprocess
import pdb
from libraries import checkreserve, getcode, log, session


# ==================================================================
#                           定数の定義
# ==================================================================
# 利用規約
RIYO_KIYAKU = "%83I%81%5B%83p%83X%81E%83X%83%7C%81%5B%83c%8E%7B%90%DD%8F%EE%95%F1%83V%83X%83e%83%80%81%40%97%98%97p%8BK%96%F1%0D%0A%0D%0A%81i%96%DA%93I%81j%0D%0A%91%E6%82P%8F%F0%81%40%82%B1%82%CC%8BK%96%F1%82%CD%81A%83I%81%5B%83p%83X%81E%83X%83%7C%81%5B%83c%8E%7B%90%DD%8F%EE%95%F1%83V%83X%83e%83%80%81i%88%C8%89%BA%81u%96%7B%83V%83X%83e%83%80%81v%82%C6%82%A2%82%A4%81B%81j%82%F0%97%98%97p%82%B5%82%C4%8E%A9%8E%A1%91%CC%81i%88%C8%89%BA%81u%8A%C7%97%9D%8E%D2%81v%82%C6%82%A2%82%A4%81B%81j%82%AA%8A%C7%97%9D%82%B7%82%E9%8C%F6%8B%A4%8E%7B%90%DD%81i%88%C8%89%BA%81u%8E%7B%90%DD%81v%82%C6%82%A2%82%A4%81B%81j%82%CC%97%98%97p%90%5C%8D%9E%82%DD%8E%E8%91%B1%93%99%81i%88%C8%89%BA%81u%97%98%97p%90%5C%8D%9E%82%DD%93%99%81v%82%C6%82%A2%82%A4%81B%81j%82%F0%8Ds%82%A4%82%BD%82%DF%82%C9%95K%97v%82%C8%8E%96%8D%80%82%C9%82%C2%82%A2%82%C4%92%E8%82%DF%82%BD%82%E0%82%CC%82%C5%82%B7%81B%0D%0A%82Q%81%40%96%7B%83V%83X%83e%83%80%82%F0%97%98%97p%82%B5%82%C4%82%A2%82%E9%8A%C7%97%9D%8E%D2%82%B2%82%C6%82%CC%97%98%97p%8E%D2%93o%98%5E%81A%8E%7B%90%DD%97%98%97p%8F%E3%82%CC%92%8D%88%D3%8E%96%8D%80%93%99%82%CD%81A%95%CA%93r%8A%C7%97%9D%8E%D2%82%CC%83z%81%5B%83%80%83y%81%5B%83W%93%99%82%F0%8EQ%8F%C6%82%B5%82%C4%82%AD%82%BE%82%B3%82%A2%81B%0D%0A%0D%0A%81i%97%98%97p%8BK%96%F1%82%CC%93%AF%88%D3%81j%0D%0A%91%E6%82Q%8F%F0%81%40%96%7B%83V%83X%83e%83%80%82%F0%97%98%97p%82%B5%82%C4%8E%7B%90%DD%82%CC%97%98%97p%90%5C%8D%9E%82%DD%93%99%82%F0%8Ds%82%A4%82%C9%82%CD%81A%82%B1%82%CC%8BK%96%F1%82%C9%93%AF%88%D3%82%B5%82%C4%82%A2%82%BD%82%BE%82%AD%82%B1%82%C6%82%AA%95K%97v%82%C5%82%B7%81B%82%B1%82%CC%82%B1%82%C6%82%F0%91O%92%F1%82%C9%81A%8A%C7%97%9D%8E%D2%82%CD%96%7B%83V%83X%83e%83%80%82%C9%82%E6%82%E9%83T%81%5B%83r%83X%82%F0%92%F1%8B%9F%82%B5%82%DC%82%B7%81B%0D%0A%82Q%81%40%89%BD%82%E7%82%A9%82%CC%97%9D%97R%82%C9%82%E6%82%E8%82%B1%82%CC%8BK%96%F1%82%C9%93%AF%88%D3%82%B7%82%E9%82%B1%82%C6%82%AA%82%C5%82%AB%82%C8%82%A2%8F%EA%8D%87%82%CD%81A%96%7B%83V%83X%83e%83%80%82%C9%82%E6%82%E9%97%98%97p%90%5C%8D%9E%82%DD%93%99%82%CD%82%C5%82%AB%82%DC%82%B9%82%F1%81B%0D%0A%0D%0A%81i%97%98%97p%82%C5%82%AB%82%E9%8C%F6%8B%A4%8E%7B%90%DD%81j%0D%0A%91%E6%82R%8F%F0%81%40%96%7B%83V%83X%83e%83%80%82%C5%97%98%97p%90%5C%8D%9E%82%DD%93%99%82%AA%82%C5%82%AB%82%E9%8E%7B%90%DD%82%C6%8B%EF%91%CC%93I%82%C8%97%98%97p%95%FB%96%40%82%C9%82%C2%82%A2%82%C4%82%CD%81A%8A%C7%97%9D%8E%D2%82%AA%95%CA%82%C9%92%E8%82%DF%82%DC%82%B7%81B%0D%0A%0D%0A%81i%97%98%97p%8E%D2%93o%98%5E%82%CC%90%5C%8D%9E%82%DD%81j%0D%0A%91%E6%82S%8F%F0%81%40%96%7B%83V%83X%83e%83%80%82%CC%97%98%97p%82%F0%8A%F3%96%5D%82%B7%82%E9%82%E0%82%CC%82%CD%96%7B%83V%83X%83e%83%80%82%CC%97%98%97p%8E%D2%93o%98%5E%90%5C%90%BF%8F%91%81i%88%C8%89%BA%81u%90%5C%90%BF%8F%91%81v%82%C6%82%A2%82%A4%81B%81j%82%F0%92%F1%8Fo%82%B5%82%C8%82%AF%82%EA%82%CE%82%C8%82%E8%82%DC%82%B9%82%F1%81B%93o%98%5E%8F%F0%8C%8F%82%E2%90%5C%8D%9E%82%DD%95%FB%96%40%93%99%82%CD%8A%C7%97%9D%8E%D2%82%C9%82%E6%82%E8%88%D9%82%C8%82%E8%82%DC%82%B7%82%CC%82%C5%8E%96%91O%82%C9%82%B2%8Am%94F%82%AD%82%BE%82%B3%82%A2%81B%0D%0A%0D%0A%81i%93o%98%5E%8E%D2%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%CC%97%98%97p%8By%82%D1%8A%C7%97%9D%81j%0D%0A%91%E6%82T%8F%F0%81%40%93o%98%5E%8E%D2%82%CD%81A%96%7B%83V%83X%83e%83%80%82%CC%97%98%97p%82%C9%82%A0%82%BD%82%C1%82%C4%82%CD%81A%93o%98%5E%8E%D2%94%D4%8D%86%81A%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%F0%93%FC%97%CD%82%B7%82%E9%82%B1%82%C6%82%C9%82%E6%82%E8%81A%97%98%97p%90%5C%8D%9E%82%DD%93%99%82%F0%8Ds%82%A4%82%B1%82%C6%82%AA%82%C5%82%AB%82%DC%82%B7%81B%0D%0A%82Q%81%40%83p%83X%83%8F%81%5B%83h%82%CD%96%7B%83V%83X%83e%83%80%82%CC%97%98%97p%82%C9%82%A0%82%BD%82%E8%81A%93o%98%5E%82%AA%95K%90%7B%82%C6%82%C8%82%E8%82%DC%82%B7%81B%83C%83%93%83%5E%81%5B%83l%83b%83g%0D%0A%81i%83p%83%5C%83R%83%93%81j%81E%8Cg%91%D1%93d%98b%81E%8AX%93%AA%92%5B%96%96%82%C5%82%CC%83V%83X%83e%83%80%83%8D%83O%83C%83%93%8E%9E%82%C9%95K%97v%82%C6%82%C8%82%E9%82W%8C%85%81%60%82P%82U%8C%85%82%CC%89p%90%94%8E%9A%82%C5%82%B7%81B%0D%0A%82R%81%40%88%C3%8F%D8%94%D4%8D%86%82%CD%81A%8AX%93%AA%92%5B%96%96%8B%40%82%C5%8F%88%97%9D%82%F0%8Am%92%E8%82%B7%82%E9%8D%DB%82%C9%93%FC%97%CD%82%C6%82%C8%82%E9%82S%8C%85%81%60%82W%8C%85%82%CC%90%94%8E%9A%82%C5%82%B7%81B%0D%0A%82S%81%40%93o%98%5E%8E%D2%82%CD%81A%93o%98%5E%8E%D2%94%D4%8D%86%81A%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%F0%8E%9F%82%CC%8E%96%8D%80%82%C9%92%8D%88%D3%82%B5%82%C4%81A%8E%A9%8C%C8%82%CC%90%D3%94C%82%C9%82%A8%82%A2%82%C4%8C%B5%8Fd%82%C9%8A%C7%97%9D%82%B5%82%C4%82%AD%82%BE%82%B3%82%A2%81B%0D%0A%81i%82P%81j%81%40%93o%98%5E%8E%D2%94%D4%8D%86%81A%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%CD%81A%91%BC%90l%82%C9%92m%82%E7%82%EA%82%C8%82%A2%82%E6%82%A4%82%C9%8A%C7%97%9D%82%B7%82%E9%82%B1%82%C6%81B%0D%0A%81i%82Q%81j%81%40%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%CD%81A%92%E8%8A%FA%93I%82%C9%95%CF%8DX%82%B5%81A%91%E6%8EO%8E%D2%82%D6%82%CC%98R%82%A6%82%A2%96h%8E%7E%82%C9%93w%82%DF%82%E9%82%B1%82%C6%81B%0D%0A%81i%82R%81j%81%40%91%BC%90l%82%A9%82%E7%82%CC%93o%98%5E%8E%D2%94%D4%8D%86%81A%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%CC%8F%C6%89%EF%82%C9%89%9E%82%B6%82%C8%82%A2%82%B1%82%C6%81B%0D%0A%81i%82S%81j%81%40%93o%98%5E%8E%D2%94%D4%8D%86%81A%88%C3%8F%D8%94%D4%8D%86%8By%82%D1%83p%83X%83%8F%81%5B%83h%82%F0%96Y%8E%B8%82%B5%82%BD%8F%EA%8D%87%82%CD%81A%91%AC%82%E2%82%A9%82%C9%81A%97%98%97p%8E%D2%93o%98%5E%82%F0%8Ds%82%C1%82%BD%8E%7B%90%DD%82%C9%98A%97%8D%82%B5%81A%82%BB%82%CC%8Ew%8E%A6%82%C9%8F%5D%82%A4%82%B1%82%C6%81B%0D%0A%0D%0A%81i%97%98%97p%8E%D2%93o%98%5E%82%CC%8E%E6%82%E8%8F%C1%82%B5%81j%0D%0A%91%E6%82U%8F%F0%81%40%93o%98%5E%8E%D2%82%AA%8E%9F%82%CC%82%A2%82%B8%82%EA%82%A9%82%C9%8AY%93%96%82%B5%82%BD%8F%EA%8D%87%82%C9%82%CD%81A%8A%C7%97%9D%8E%D2%82%CD%82%BB%82%CC%93o%98%5E%8E%D2%82%CC%97%98%97p%8E%D2%93o%98%5E%82%F0%8E%E6%82%E8%8F%C1%82%B5%82%DC%82%B7%81B%0D%0A%81i%82P%81j%81%40%8B%95%8BU%82%CC%90%5C%8D%90%82%F0%82%B5%82%BD%8F%EA%8D%87%0D%0A%81i%82Q%81j%81%40%82%B1%82%CC%8BK%96%F1%82%C9%88%E1%94%BD%82%B5%82%BD%8F%EA%8D%87%0D%0A%81i%82R%81j%81%40%96%7B%83V%83X%83e%83%80%82%C9%91%CE%82%B5%81A%95s%90%B3%82%C9%83A%83N%83Z%83X%82%B5%82%BD%8F%EA%8D%87%0D%0A%81i%82S%81j++%89%DF%8F%E8%82%C8%83A%83N%83Z%83X%81i%8E%A9%93%AE%8F%84%89%F1%83c%81%5B%83%8B%81A%83N%83%8D%81%5B%83%89%81%5B%81A%83%8D%83%7B%83b%83g%81A%82%BB%82%CC%91%BC%95s%90%B3%82%C8%83c%81%5B%83%8B%81j%82%C9%82%E6%82%E8%81A%96%7B%83V%83X%83e%83%80%82%CC%8F%88%97%9D%82%C9%89e%8B%BF%82%F0%97%5E%82%A6%82%E9%82%C6%8A%C7%97%9D%8E%D2%82%AA%94%BB%92f%82%B5%82%BD%8F%EA%8D%87%0D%0A%81i%82T%81j%81%40%96%7B%83V%83X%83e%83%80%82%CC%8A%C7%97%9D%8By%82%D1%89%5E%89c%82%F0%8C%CC%88%D3%82%C9%96W%8AQ%82%B5%82%BD%8F%EA%8D%87%0D%0A%81i%82U%81j%81%40%91O%8D%86%82%C9%8Cf%82%B0%82%E9%82%E0%82%CC%82%CC%91%BC%81A%8A%C7%97%9D%8E%D2%82%AA%81A%93o%98%5E%8E%D2%82%C6%82%B5%82%C4%95s%93K%93%96%82%C6%94F%82%DF%82%BD%8F%EA%8D%87%0D%0A%0D%0A%81i%97%98%97p%8E%9E%8A%D4%81j%0D%0A%91%E6%82V%8F%F0%81%40%96%7B%83V%83X%83e%83%80%82%CC%97%98%97p%8E%9E%8A%D4%82%CD%81A%94N%96%96%81E%94N%8En%81i%82P%82Q%8C%8E%82R%82O%93%FA%8C%DF%91O%82O%8E%9E%81%60%82P%8C%8E%82S%93%FA%8C%DF%91O%82X%8E%9E%81j%82%F0%8F%9C%82%AB%81A%82%A2%82%C2%82%C5%82%E0%97%98%97p%82%C5%82%AB%82%DC%82%B7%81B%82%BD%82%BE%82%B5%81A%96%88%8C%8E%82Q%82T%93%FA%8C%DF%91O%82O%8E%9E%81%60%8C%DF%91O%82T%8E%9E%82%CC%8A%D4%82%CD%97%98%97p%82%C5%82%AB%82%DC%82%B9%82%F1%81B%0D%0A%82%C8%82%A8%81A%83V%83X%83e%83%80%89%5E%89c%8F%E3%82%CC%93_%8C%9F%82%E2%8DH%8E%96%82%CC%82%BD%82%DF%81A%88%EA%95%94%82%DC%82%BD%82%CD%91S%95%94%82%CC%83T%81%5B%83r%83X%82%F0%92%E2%8E%7E%82%B7%82%E9%8F%EA%8D%87%82%AA%82%A0%82%E8%82%DC%82%B7%81B%0D%0A%0D%0A%81i%96%C6%90%D3%8E%96%8D%80%81j%0D%0A%91%E6%82W%8F%F0%81%40%8A%C7%97%9D%8E%D2%82%CD%81A%93o%98%5E%8E%D2%82%AA%96%7B%83V%83X%83e%83%80%82%F0%97%98%97p%82%B5%82%BD%82%B1%82%C6%82%C9%82%E6%82%E8%94%AD%90%B6%82%B5%82%BD%93o%98%5E%8E%D2%82%CC%91%B9%8AQ%8By%82%D1%93o%98%5E%8E%D2%82%AA%91%E6%8EO%8E%D2%82%C9%97%5E%82%A6%82%BD%91%B9%8AQ%82%C9%82%C2%82%A2%82%C4%81A%88%EA%90%D8%82%CC%90%D3%94C%82%F0%95%89%82%A2%82%DC%82%B9%82%F1%81B%0D%0A%82Q%81%40%8A%C7%97%9D%8E%D2%82%CD%81A%96%7B%83V%83X%83e%83%80%82%CC%89%5E%97p%82%CC%92%E2%8E%7E%81A%92%86%8E%7E%96%94%82%CD%92%86%92f%93%99%82%C9%82%E6%82%E8%93o%98%5E%8E%D2%82%C9%94%AD%90%B6%82%B5%82%BD%91%B9%8AQ%82%C9%82%C2%82%A2%82%C4%81A%88%EA%90%D8%82%CC%90%D3%94C%82%F0%95%89%82%A2%82%DC%82%B9%82%F1%81B%0D%0A%0D%0A%81i%8C%C2%90l%8F%EE%95%F1%82%CC%95%DB%8C%EC%81j%0D%0A%91%E6%82X%8F%F0%81%40%93o%98%5E%8E%D2%82%CC%90%5C%8D%9E%82%DD%82%C9%8A%EE%82%C3%82%AD%8C%C2%90l%8F%EE%95%F1%82%C9%82%C2%82%A2%82%C4%81A%8A%C7%97%9D%8E%D2%82%CD%81A%96%7B%97%88%82%CC%96%DA%93I%88%C8%8AO%82%C9%8Eg%97p%82%B9%82%B8%81A%82%BB%82%CC%8A%C7%97%9D%82%C9%8F%5C%95%AA%82%C8%92%8D%88%D3%82%F0%95%A5%82%A2%82%DC%82%B7%81B%0D%0A%82Q%81%40%8A%C7%97%9D%8E%D2%82%CD%81A%93o%98%5E%8E%D2%82%CC%90%5C%8D%9E%82%DD%82%C9%8A%EE%82%C3%82%AD%8C%C2%90l%8F%EE%95%F1%82%C9%82%C2%82%A2%82%C4%81A%8C%C2%90l%8F%EE%95%F1%95%DB%8C%EC%82%C9%95K%97v%82%C8%91%5B%92u%82%F0%8Du%82%B6%82%BD%82%A4%82%A6%82%C5%81A%96%7B%83V%83X%83e%83%80%82%CC%89%5E%97p%82%C9%95K%97v%82%C8%94%CD%88%CD%82%C9%8C%C0%82%E8%81A%8Ae%8E%7B%90%DD%82%C5%82%CC%8B%A4%92%CA%8F%EE%95%F1%82%C6%82%B5%82%C4%8Ae%8E%7B%90%DD%82%CC%8A%C7%97%9D%8E%D2%82%AA%97%98%97p%82%B7%82%E9%8F%EA%8D%87%82%AA%82%A0%82%E8%82%DC%82%B7%81B%0D%0A%0D%0A%81i%93o%98%5E%8F%EE%95%F1%82%CC%8E%9A%91%CC%81j%0D%0A%91%E6%82P%82O%8F%F0%81%40%92%F1%8Fo%82%B3%82%EA%82%BD%90%5C%8D%9E%8F%91%82%CC%8BL%93%FC%8E%9A%91%CC%82%C9%82%C2%82%A2%82%C4%81A%96%7B%83V%83X%83e%83%80%82%C5%82%CC%8E%E6%88%B5%82%A2%82%AA%8D%A2%93%EF%82%C5%82%A0%82%E9%8F%EA%8D%87%82%CD%81A%96%7B%83V%83X%83e%83%80%82%C5%95%5C%8E%A6%82%B3%82%EA%82%E9%8E%9A%91%CC%81i%95W%8F%80%95%B6%8E%9A%81j%82%C9%82%C8%82%E8%82%DC%82%B7%81B%0D%0A%0D%0A%81i%97%98%97p%8BK%96%F1%82%CC%95%CF%8DX%81j%0D%0A%91%E6%82P%82P%8F%F0%81%40%8A%C7%97%9D%8E%D2%82%CD%81A%95K%97v%82%AA%82%A0%82%E9%82%C6%94F%82%DF%82%E9%82%C6%82%AB%82%CD%81A%93o%98%5E%8E%D2%82%D6%82%CC%8E%96%91O%82%CC%92%CA%92m%82%F0%8Ds%82%A4%82%B1%82%C6%82%C8%82%AD%81A%82%B1%82%CC%8BK%96%F1%82%F0%95%CF%8DX%82%C5%82%AB%82%E9%82%E0%82%CC%82%C6%82%B5%82%DC%82%B7%81B%0D%0A%82Q%81%40%93o%98%5E%8E%D2%82%CD%81A%97%98%97p%82%CC%93s%93x%81A%82%B1%82%CC%8BK%96%F1%82%F0%8Am%94F%82%B7%82%E9%82%B1%82%C6%82%C6%82%B5%81A%82%B1%82%CC%8BK%96%F1%95%CF%8DX%8C%E3%82%C9%96%7B%83V%83X%83e%83%80%82%F0%97%98%97p%82%B5%82%BD%8F%EA%8D%87%82%CD%81A%95%CF%8DX%8C%E3%82%CC%8BK%96%F1%82%C9%93%AF%88%D3%82%B5%82%BD%82%E0%82%CC%82%C6%82%B5%82%DC%82%B7%81B%0D%0A%0D%0A%81i%82%BB%82%CC%91%BC%81j%0D%0A%91%E6%82P%82Q%8F%F0%81%40%82%B1%82%CC%8BK%96%F1%82%C9%92%E8%82%DF%82%CC%82%C8%82%A2%8E%96%8D%80%82%BB%82%CC%91%BC%95K%97v%82%C8%8E%96%8D%80%82%C9%82%C2%82%A2%82%C4%82%CD%81A%8A%C7%97%9D%8E%D2%82%AA%95%CA%82%C9%92%E8%82%DF%82%E9%82%E0%82%CC%82%C6%82%B5%82%DC%82%B7%81B%0D%0A%0D%0A%95%8D%91%A5%0D%0A%82%B1%82%CC%8BK%96%F1%82%CD%81A%95%BD%90%AC%82Q%82S%94N%82P%8C%8E%82U%93%FA%82%A9%82%E7%8E%7B%8Ds%82%B5%82%DC%82%B7%81B%0D%0A"

# ユーザー情報
ID = ""
PASSWORD = ""


# =================================================================================
#                              関数の定義
# =================================================================================

# URL, データセット
def GetData(num, referrer, sessID, code=None, day=None, time=None, captcha=None, token=None):
    today = datetime.datetime.now().strftime('%Y%m')
    
    if num == 0:
        url = "https://reserve.opas.jp/osakashi/menu/Login.cgi"
    elif num == 1:
        url = "https://reserve.opas.jp/osakashi/menu/Menu.cgi"
    elif num == 2:
        url = "https://reserve.opas.jp/osakashi/yoyaku/QueryMethodSelect.cgi"
    elif num == 3:
        url = "https://reserve.opas.jp/osakashi/yoyaku/GenreSelect.cgi"
    elif num == 4:
        url = "https://reserve.opas.jp/osakashi/yoyaku/GenreSelect.cgi"
    elif num == 5:
        url = "https://reserve.opas.jp/osakashi/yoyaku/ShisetsuMultiSelect.cgi"
    elif num == 6:
        url = "https://reserve.opas.jp/osakashi/yoyaku/CalendarStatusSelect.cgi"
    elif num == 7:
        url = "https://reserve.opas.jp/osakashi/yoyaku/CalendarStatusSelect.cgi"
    elif num == 8:
        url = "https://reserve.opas.jp/osakashi/yoyaku/ShinseiEntry.cgi"
    elif num == 9:
        url = "https://reserve.opas.jp/osakashi/yoyaku/PriceConfirm.cgi"
    elif num == 98:
        url = "https://reserve.opas.jp/osakashi/menu/Menu.cgi"
    elif num == 99:
        url = "https://reserve.opas.jp/osakashi/yoyaku/RiyoshaYoyakuList.cgi"
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": sessID + " ROUTEID=.r1; vyrqgyw=RIYOSHA-WEB4; _ga=GA1.3.1548849856.1589966404; _gid=GA1.3.1489916570.1589966404; _gat_UA-123480356-1=1",
        "Host": "reserve.opas.jp",
        "Origin": "https://reserve.opas.jp",
        "Referer": referrer,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
    }
    
    if num == 0:
        data = {
            "action": "Enter",
            "txtProcId": "%2Fmenu%2FLogin",
            "txtRiyoshaCode": ID,
            "txtPassWord": PASSWORD
        }
    elif num == 1:
        data = {
            "action":"Enter",
            "txtProcId":"/menu/Menu",
            "txtFunctionCode":"Yoyaku"
        }
    elif num == 2:
        data = {
            "action":"Enter",
            "txtProcId":"/yoyaku/QueryMethodSelect",
            "txtSelectKey":"0"
        }
    elif num == 3:
        data = {
            "action":"Enter",
            "txtProcId":"/yoyaku/GenreSelect",
            "gamenNo":"0",
            "metaShubetsuCd":"C00"
        }
    elif num == 4:
        data = {
            "action":"Enter",
            "txtProcId":"/yoyaku/GenreSelect",
            "gamenNo":"1",
            "shubetsuCd":"C01"
        }
    elif num == 5:
        data = {
            "action":"Enter",
            "txtProcId":"/yoyaku/ShisetsuMultiSelect",
            "checkMeisaiUniqKey":code
        }
    elif num == 6:
        data = {
            "action":"Setup",
            "txtProcId":"/yoyaku/CalendarStatusSelect",
            "txtCalYobiView":"block",
            "printedFlg":"",
            "radioshow":"week",
            "optYear":day[0:4],
            "optMonth":day[4:6],
            "optDay":day[6:8],
            "txtYear":"",
            "txtMonth":"",
            "txtDay":"",
            "checkShowDay":["MON","TUE","WED","THU","FRI","SAT","SUN","HOL"]
        }
    elif num == 7:
        data = {
            "action":"Enter",
            "txtProcId":"/yoyaku/CalendarStatusSelect",
            "txtCalYobiView":"block",
            "printedFlg":"",
            "radioshow":"week",
            "optYear":day[0:4],
            "optMonth":day[4:6],
            "optDay":day[6:8],
            "txtYear":"",
            "txtMonth":"",
            "txtDay":"",
            "checkShowDay":["MON","TUE","WED","THU","FRI","SAT","SUN","HOL"],
            "checkYoyakuStatus":code[0:19] + "_0000_" + day + "_" + time + ":" + time + getcode.GetYoyakuCode(code) + getcode.GetReserveTime(time)
        }
    elif num == 8:
        data = {
            "org.apache.struts.taglib.html.TOKEN":token,
            "action":"Enter",
            "txtProcId":"/yoyaku/ShinseiEntry",
            "inputMensu":"1",
            "numberOfRiyosha":"20",
            "checkFavorite":"0"
        }
    elif num == 9:
        data = {
            "org.apache.struts.taglib.html.TOKEN":token,
            "action":"Enter",
            "txtProcId":"/yoyaku/PriceConfirm",
            "riyobiShiseMomethod":"0",
            "txtAgreement":RIYO_KIYAKU,
            "chkRiyoKiyaku":"1",
            "txtKaptcha":captcha
            
        }
    elif num == 98:
        data = {
            "action":"Enter",
            "txtProcId":"/menu/Menu",
            "txtFunctionCode":"YoyakuQuery"
        }
    elif num == 99:
        data = {
            "action":"Setup",
            "txtProcId":"/yoyaku/RiyoshaYoyakuList",
            "selectedYoyakuUniqKey":"",
            "hiddenCorrectRiyoShinseiYM":"",
            "hiddenCollectDisplayNum":"100",
            "pageIndex":"0",
            "printedFlg":"",
            "riyoShinseiYM":day[0:6],
            "txtRiyoShinseiYM":today[0:4] + "%94N"+ today[4:6] +"%8C%8E",
            "reqDisplayInfoNum":"100",
            "txtReqDisplayInfoNum":""
        }
    
    return url, headers, data


# セッションIDの取得
def GetSessionID(resp):
    start  = resp.headers['Set-Cookie'].find("JSESSIONID=", 2)
    finish = resp.headers['Set-Cookie'].find(";", start)
    sessID = resp.headers['Set-Cookie'][start:finish+1]
    
    return sessID

# トークンの取得
def GetToken(resp):
    start = resp.text.find("org.apache.struts.taglib.html.TOKEN")
    start = resp.text.find("value=", start) + 7
    finish = resp.text.find('"', start)
    token = resp.text[start:finish]
    
    return token

# Captcha画像のダウンロード
def DownloadImage(sess, savePath):
    url = "https://reserve.opas.jp/osakashi/kaptcha.jpg"
    
    resp = sess.get(url, stream=True)
    
    with open(savePath, 'wb') as f:
        f.raw.decode_content = True
        shutil.copyfileobj(resp.raw, f)
        

# キャプチャ突破
def BreakCaptcha(sess, path):
    DownloadImage(sess, "./image/" + path)
    
    cmd = "magick convert " + "./image/" + path + " -crop 165x50+45+0 -negate -morphology erode octagon:2 -negate -threshold 78% " + "./image_conv/conv_" + path
    subprocess.call(cmd, shell=True)
    cmd = 'tesseract --psm 7 ' + './image_conv/conv_' + path + ' out -c tessedit_char_whitelist="23456789abcdefghkmnprstuvwxyz" -l eng'
    subprocess.call(cmd, shell=True)
    with open("./out.txt") as f0:
        str = ProcessStr(f0.readline())
        with open("./out_list.txt", mode='a') as f1:
            f1.write(log.Now() + " Path:" + path + " Text:" + str + "\n")
    
    return str

# 文字調整
def ProcessStr(str):
    str_array = "23456789abcdefghkmnprstuvwxyz"
    result = ""
    for char in str:
        if (str_array.find(char) != -1):
            result = result + char
    return result

# =================================================================================

# メイン処理
def main(str_code):
    main_sess = session.session()
    sub_sess  = session.session()
    
    # 初期設定
    code = getcode.GetGymCode(str_code[0:2])
    day  = str_code[2:10]
    time = str_code[10:11]
    
    # ログイン
    main_sess.setPostParam(GetData(0, main_sess.referrer, main_sess.sessID))
    main_sess.PostData()
    main_sess.setSessionID(GetSessionID(main_sess.resp))
    
    # サブログイン
    sub_sess.setPostParam(GetData(0, sub_sess.referrer, sub_sess.sessID))
    sub_sess.PostData()
    sub_sess.setSessionID(GetSessionID(sub_sess.resp))
    
    # メニュー遷移
    sub_sess.setPostParam(GetData(98, sub_sess.referrer, sub_sess.sessID))
    sub_sess.PostData()
    
    # 小分類選択
    main_sess.setPostParam(GetData(4, main_sess.referrer, main_sess.sessID))
    main_sess.PostData()
    
    
    # 体育館選択
    main_sess.setPostParam(GetData(5, main_sess.referrer, main_sess.sessID, code=code))
    main_sess.PostData()
    
    
    # 日付表示
    main_sess.setPostParam(GetData(6, main_sess.referrer, main_sess.sessID, day=day))
    main_sess.PostData()
    
    
    # 日付選択
    main_sess.setPostParam(GetData(7, main_sess.referrer, main_sess.sessID, code=code, day=day, time=time))
    main_sess.PostData()
    
    
    # 面数、人数確定
    main_sess.setPostParam(GetData(8, main_sess.referrer, main_sess.sessID, token=GetToken(main_sess.resp)))
    main_sess.PostData()
    
    
    # 予約確定
    i = 0
    chk = False
    while(main_sess.resp.text.find("公共施設予約システム（エラー情報）") == -1 and main_sess.resp.text.find("公共施設予約システム（予約完了）") == -1 and not chk and i < 10):
        captcha = BreakCaptcha(main_sess.sess, "captcha" + '{:0=3}'.format(i) + ".jpg")
        main_sess.setPostParam(GetData(9, main_sess.referrer, main_sess.sessID, token=GetToken(main_sess.resp), captcha=captcha))
        
        # リファラーのバックアップ
        tmp = main_sess.referrer
        main_sess.PostData()
        # リファラーのリストア
        main_sess.referrer = tmp
        
        # 予約が完了しているか確認
        sub_sess.setPostParam(GetData(99, sub_sess.referrer, sub_sess.sessID, day=day))
        sub_sess.PostData()
        if (checkreserve.CheckReserve(sub_sess.resp, code, day, time)):
            chk = True
        
        i = i + 1
    
    with open("./result.txt") as res:
        if (chk):
            res.write(str_code + ":  ○")
        else:
            res.write(str_code + ":  ×")

if __name__=='__main__':
    log.OutTitle("==================================================")
    log.OutTitle("                 処 理 開 始                      ")
    log.OutTitle("==================================================")
    with open("./input.txt") as f:
        for str_line in f:
            main(str_line)
    log.OutTitle("==================================================")
    log.OutTitle("                 処 理 終 了                      ")
    log.OutTitle("==================================================")

