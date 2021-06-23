#############################################
# AB TESTİNG PROJECT
#############################################

# Kütüphaneler
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

Control_df = pd.read_excel("HAFTA_05/ab_testing.xlsx", sheet_name="Control Group")
Test_df = pd.read_excel("HAFTA_05/ab_testing.xlsx", sheet_name="Test Group")

Control_df.head()
Test_df.head()

#######################
# Verinin yapısal bilgilerinin incelenmesi:
#######################
from helpers.helpers import check_df, retail_data_prep, grab_col_names, num_summary, cat_summary
check_df(Control_df)
check_df(Test_df)

cat_cols, num_cols, cat_but_car = grab_col_names(Control_df)
cat_cols, num_cols, cat_but_car = grab_col_names(Test_df)

for col in num_cols:
    print({f"{col}"})
    num_summary(Control_df, col)

for col in num_cols:
    print({f"{col}"})
    num_summary(Test_df, col)

#######################
# Betimsel istatistikleri
#######################
Control_df.describe().T
Test_df.describe().T

# Satın almaya göre ortalama kazanç?
Control_df.groupby("Purchase", as_index=False).agg({"Earning": "mean"}).sort_values(by="Earning", ascending=False).head()
Test_df.groupby("Purchase", as_index=False).agg({"Earning": "mean"}).sort_values(by="Earning", ascending=False).head()

# Tıklanmaya göre ortalama kazanç?
Control_df.groupby("Click", as_index=False).agg({"Earning": "mean"}).sort_values(by="Earning", ascending=False).head()
Test_df.groupby("Click", as_index=False).agg({"Earning": "mean"}).sort_values(by="Earning", ascending=False).head()

#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# Görev 1: A/B testinin hipotezini tanımlama:
#############################################

########################
# Hipotezi Kurma:
########################
# H0 : M1=M2 (Yeni özellik ile eski özellik arasında istatistiksel olarak anlamlı bir farklılık yoktur.)
# H1 : M1!=M2 (..vardır.)

# Aralarında fark var gibi gözüküyor ama şans eseri ortaya çıkmış olabilir.
# Matematiksel olarak fark var gibi gözüküyor, istatistikçesi fark olup olmadığını bilinmiyor o yüzden incelemek gerekiyor.
Control_df["Purchase"].mean()
Test_df["Purchase"].mean()

# Dağılımlarını inceleme:
def graphic(dataframe, col):
    sns.distplot(dataframe[col])
    plt.show()

graphic(Test_df, "Purchase")
graphic(Control_df, "Purchase")

#############################################
# Görev 2: Hipotez testini gerçekleştirme ve yorumlama:
#############################################

########################
# Normallik Varsayımı:
########################
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = shapiro(Control_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))  # H0: Reddedilemez. Normallik varsayımı sağlanmaktadır.

test_stat, pvalue = shapiro(Test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))  # H0: Reddedilemez. Normallik varsayımı sağlanmaktadır.

########################
# Varyans Homojenligi Varsayımı:
########################
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(Control_df["Purchase"],
                           Test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # H0: Reddedilemez  varyanslar homojendir

########################
#  Varsayımlar sağlanıyorsa Bağımsız İki Örneklem T Testi (parametrik test)
########################
test_stat, pvalue = ttest_ind(Control_df["Purchase"],
                              Test_df["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # H0: Reddedilemez.
# Test ve Control grupları arasında %95 güven ile istatistiksel olarak anlamlı bir farklılık yoktur.

#############################################
# Görev 3: Kullanılan testleri belirtme:
#############################################
# Normallik varsayımı için shapiro kullanıldı.
# Varyans homojenliği için levene kullanıldı.
# Normallik ve varyans homojenliği varsayımları sağlandığı için parametrik test olan Bağımsız İki Örneklem T Testi kullanıldı.

########################
# Fonksiyonlaştırma:
########################
def way(dataframe1, dataframe2, col_name):
    pvalue1 = shapiro(dataframe1[col_name])[1]
    pvalue2 = shapiro(dataframe2[col_name])[1]
    pvalue3 = levene(dataframe1[col_name], dataframe2[col_name])[1]
    pvalue4 = mannwhitneyu(dataframe1[col_name], dataframe2[col_name])[1]
    a = ttest_ind(dataframe1[col_name], dataframe2[col_name], equal_var=True)[1]
    b = ttest_ind(dataframe1[col_name], dataframe2[col_name], equal_var=False)[1]
    if (pvalue1 and pvalue2) > 0.05:
        # varsayımlar homojen ise
        if pvalue3 > 0.05:
            if a > 0.05:
                print('ttest sonucu p-value = %.4f' % (a))
                print(F"H0  Reddedilemez ve iki özellik arasında anlamlı bir farklılık yoktur")
            else:
                print('ttest sonucu p-value = %.4f' % (a))
                print(F"H0 Red ve iki özellik arasında anlamlı bir farklılık vardır")
        # Varsayımlar homojen değil ise
        else:
            if b > 0.05:
                print('ttest sonucu p-value = %.4f' % (b))
                print(F"H0 Reddedilemez ve ki özellik arasında anlamlı bir farklılık yoktur")
            else:
                print('ttest sonucu p-value = %.4f' % (b))
                print(F"H0 Red ve iki özellik arasında anlamlı bir farklılık vardır")
    # Normallik varsayımı sağlanmıyor ise
    else:
        if pvalue4 > 0.05:
            print('mannwhitneyu sonucu p-value = %.4f' % (pvalue4))
            print(F"H0 Reddedilemez ve iki özellik arasında anlamlı bir farklılık yoktur")
        else:
            print('mannwhitneyu sonucu p-value = %.4f' % (pvalue4))
            print(F"H0 Red ve iki özellik arasında anlamlı bir farklılık vardır")

way(Control_df, Test_df, "Earning")
way(Control_df, Test_df, "Purchase")
way(Control_df, Test_df, "Click")
way(Control_df, Test_df, "Impression")

col_names = [col for col in Test_df.columns if col in Control_df.columns]
for col in col_names:
    print(F" {col.upper()} ".center(50, "*"))
    way(Control_df, Test_df, col)

"""
******************* IMPRESSION *******************
ttest sonucu p-value = 0.0000
H0 Red ve iki özellik arasında anlamlı bir farklılık vardır
********************* CLICK **********************
ttest sonucu p-value = 0.0000
H0 Red ve iki özellik arasında anlamlı bir farklılık vardır
******************** PURCHASE ********************
ttest sonucu p-value = 0.3493
H0  Reddedilemez ve iki özellik arasında anlamlı bir farklılık yoktur
******************** EARNING *********************
ttest sonucu p-value = 0.0000
H0 Red ve iki özellik arasında anlamlı bir farklılık vardır
"""

#############################################
# Görev 4:Görev 2’de verilen cevaba göre, müşteriye tavsiye ne olmalı?
#############################################
# Purchase değişkeni üzerinden gidilirse iki özellik arasında matematiksel olarak bir fark vardır fakat anlamlı bir farklılık bulunmamaktadır.
# Diğer değişkenler üzerinden gidilirse Web sitesinde daha çok trafik oluşturmak için bu yöntemi tercih etmeleri faydalı olabilir.