#####################################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olanbombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için birA/B testiyapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.


#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Proje Görevleri
#####################################################

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("CaseStudy-1(ABTesti)/ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("CaseStudy-1(ABTesti)/ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

check_df(df_control)
check_df(df_test)


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
# Hangi verinin hangi gruptan geldiğini belirlemek için ayrı bir stun oluşturup bu stuna grubun ismini atıyoruz.

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()
df.tail()




#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)


# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("group").agg({"Purchase": "mean"})

#          Purchase
# group
# control  550.89406
# test     582.10610

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz
# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-valuedeğerlerini yorumlayınız.


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO reddedilemez. Control grubunun değerleri normal dağılım varsayımını sağlamaktadır.


# Varyans Homojenliği :
# H0: Varyanslarhomojendir.
# H1: Varyanslarhomojen Değildir.
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-valuedeğerlerini yorumlayınız.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO reddedilemez. Control ve Test grubunun değerleri varyans homejenliği varsayımını sağlamaktadır.
# Varyanslar Homojendir.

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapılmaktadır.
# H0: M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark vardır)
# p<0.05 HO RED , p>0.05 HO REDDEDİLEMEZ

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# p-value=0.3493
# HO reddedilemez. Kontrol ve test grubu satın alma ortalamaları arasında istatistiksel olarak anlamlı farklılık yoktur.


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

##################################### Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.####################################

# Kontrol ve test gruplarının “Purchase” (satın alma) ortalamaları arasında anlamlı bir fark olup olmadığını test etmek için
# bağımsız iki örneklem t-testi (Independent Samples t-test) kullanılmıştır.
# Bu testin seçilme sebebi, öncelikle t-testi öncesi varsayımların kontrol edilmesiyle ilgilidir:

# Normallik varsayımı: Her iki grup için ayrı ayrı yapılan Shapiro-Wilk testi sonucunda p-değerleri 0.05’ten büyük çıkmış,
# bu da verilerin normal dağıldığını göstermiştir.
# Varyans homojenliği varsayımı: Levene testi ile kontrol edilmiş ve yine p > 0.05 olduğu için iki grup arasındaki varyansların
# eşit olduğu kabul edilmiştir.

# Her iki varsayım da sağlandığı için parametrik test olan bağımsız t-testi kullanılması uygun bulunmuştur.


########################## Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz. ##########################

# T-testi sonucunda elde edilen p-değeri = 0.3493, yani 0.05’ten büyüktür. Bu durumda H0 hipotezi reddedilemez,
# yani kontrol ve test gruplarının ortalama satın alma değerleri arasında istatistiksel olarak anlamlı bir fark bulunmamaktadır.

# Bu sonuçlara göre, müşteriye şu şekilde tavsiyede bulunulabilir:

# Yeni teklif stratejisi (test grubu) ile mevcut strateji (kontrol grubu) arasında satın alma açısından anlamlı bir fark gözlemlenmemiştir.
# Bu nedenle, yeni teklif stratejisi daha maliyetli veya karmaşıksa uygulanmasına gerek olmayabilir.
# Ancak farklı metrikler (örneğin müşteri memnuniyeti, uzun vadeli etki vb.) de dikkate alınarak karar verilmesi önerilir.