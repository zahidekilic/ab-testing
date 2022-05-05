########### İŞ PROBLEMİ ##############
# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan "averagebidding"’i tanıttı.
# Müşterilerimizden biri olan xyz.com, bu yeni özelliği test etmeye karar verdi ve
# averagebidding'in maximumbidding'den daha fazla dönüşüm getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.
# A/B testi 1 aydır devam ediyor ve xyz.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.


######### VERİ SETİ HİKAYESİ###########
# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra
# buradan gelen kazanç bilgileri yer almaktadır.
# Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır.
# Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer almaktadır.
# Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.
# DEĞİŞKENLER
# Impression : Reklam görüntüleme sayısı
# Click : Görüntülenen reklama tıklama sayısı
# Purchase : Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç
import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

### Veriyi Hazırlama ve Analiz Etme
kontrol = pd.read_excel("ab_testing_veri/ab_testing.xlsx", sheet_name="Control Group") #MaximumBidding
kontrol["type"] = "MaximumBidding"
test = pd.read_excel("ab_testing_veri/ab_testing.xlsx", sheet_name="Test Group") #AverageBidding
test["type"] = "AverageBidding"

kontrol.head()
kontrol["Purchase"].mean()
kontrol.describe().T
test.head()
test["Purchase"].mean()
test.describe().T

# Her iki grubu tek dataframe'de birleştiriyoruz.
df = pd.concat([kontrol,test])
df.head()
df.shape


####### A/B Testinin Hipotezinin Tanımlanması
# Hipotez : averagebidding ve maximumbidding'in getirdiği gelirde istatistiksel olarak anlamlı bir fark var mıdır?
# H0 : M1 = M2 (averagebidding ve maximumbidding'in getirdiği gelirde istatistiksel olarak anlamlı bir fark yoktur)
# H1 : M1!= M2 ((averagebidding ve maximumbidding'in getirdiği gelirde istatistiksel olarak anlamlı bir fark vardır)

kontrol["Purchase"].mean()
df.loc[df["type"] == "MaximumBidding", :]["Purchase"].mean()
test["Purchase"].mean()
df.loc[df["type"] == "AverageBidding", :]["Purchase"].mean()

#########Hipotez Testinin Gerçekleştirilmesi
# Varsayım Kontrolleri

# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = shapiro(df.loc[df["type"] == "MaximumBidding", "Purchase"])
print("Test Stat = %.4f, p-value= %.4f" % (test_stat, pvalue)) #Test Stat = 0.9773, p-value= 0.5891 -->H0 REDDEDİLEMEZ
test_stat, pvalue = shapiro(df.loc[df["type"] == "AverageBidding", "Purchase"])
print("Test Stat = %.4f, p-value= %.4f" % (test_stat, pvalue)) #Test Stat = 0.9589, p-value= 0.1541 -->H0 REDDEDİLEMEZ
#Normallik Varsayımı sağlanmaktadır.


# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = levene(df.loc[df["type"] == "MaximumBidding", "Purchase"],
                           df.loc[df["type"] == "AverageBidding", "Purchase"])
print("Test Stat = %.4f, p-value= %.4f" % (test_stat, pvalue)) # Test Stat = 2.6393, p-value= 0.1083 -->H0 REDDEDİLEMEZ
#Varyans Homojenliği Varsayımı sağlanmaktadır.


# Hipotez Testi
test_stat, pvalue = ttest_ind(df.loc[df["type"] == "MaximumBidding", "Purchase"],
                           df.loc[df["type"] == "AverageBidding", "Purchase"],
                              equal_var=True)
print("Test Stat = %.4f, p-value= %.4f" % (test_stat, pvalue)) #Test Stat = -0.9416, p-value= 0.3493 -->H0 REDDEDİLEMEZ


# Test sonuçlarına göre Test Stat = -0.9416, p-value= 0.3493 çıkmıştır. Yani H0 REDDEDİLEMEZ.
# averagebidding ve maximumbidding'in getirdiği gelirde istatistiksel olarak anlamlı bir fark yoktur.


############# Sonuçların Analizi
# Averagebidding ile maximumbidding'in getirdiği gelirde 1 aylık sonuçlar bakımından istatistiksel olarak anlamlı bir fark görülmedi.
# Ancak bunun sebebi ölçüm yapılan zamanın kısıtlı tutulmuş olması olabilir, dolayısıyla daha uzun vadede testin tekrarlanmasında fayda vardır.

