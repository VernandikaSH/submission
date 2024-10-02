import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")


# fungsi untuk mengirim nilai review yang diisi konsumen
def create_byreviewscore(df):
    byreviewscore_df = df.groupby(by="review_score").review_id.nunique().reset_index()
    byreviewscore_df.rename(columns={"review_id": "customer_count"}, inplace=True)

    byreviewscore_df["review_score"] = byreviewscore_df["review_score"].astype(str)
    byreviewscore_df["review_score"] = pd.Categorical(
        byreviewscore_df["review_score"],
        categories=["1", "2", "3", "4", "5"],
        ordered=True,
    )

    return byreviewscore_df


# fungsi untuk mengirim jumlah konsumen berdasarkan asal state
def create_bystate(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return bystate_df


# fungsi untuk mengirim jumlah konsumen berdasarkan asal kota
def create_bycity(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return bycity_df


# membaca dataset utama yang sudah menyatukan dataset-dataset yang diproses
main_data = pd.read_csv("main_data.csv")

# header untuk halaman
st.header("Analisis Data E-Commerce Public Dataset")

# subheader menampilkan jumlah konsumen berdasarkan asal lokasi
st.subheader("Jumlah Pelanggan Berdasarkan Kondisi Demografis")

# membuat tab untuk berpindah antara state, dan kota
tab1, tab2 = st.tabs(["By State", "By City"])

with tab1:
    # judul untuk jumlah konsumen berdasarkan state
    st.text("Jumlah Pelanggan Berdasarkan State")

    # menjalankan fungsi jumlah konsumen berdasarkan state ke dalam variabel bystate_df
    bystate_df = create_bystate(main_data)

    # variabel untuk menandakan persentil 75 dari bystate_df
    percentile_75 = bystate_df["customer_count"].quantile(0.75)

    # hanya menampilkan data yang diatas atau sama dengan persentil 75
    filtered_bystate_df = bystate_df[bystate_df["customer_count"] >= percentile_75]

    # membuat ukuran figure untuk menyimpan grafik
    plt.figure(figsize=(12, 5))

    # menampilkan warna khusus untuk data pertama (jumlah terbanyak)
    colors_ = [
        "#72BCD4" if i == 0 else "#D3D3D3" for i in range(len(filtered_bystate_df))
    ]

    # menentukan x dan y dari bar chart
    ax = sns.barplot(
        x="customer_count",
        y="customer_state",
        data=filtered_bystate_df.sort_values(by="customer_count", ascending=False),
        palette=colors_,
    )

    # mengatur dan menampilkan informasi-informasi yang dibutuhkan
    plt.title("Jumlah Pelanggan Berdasarkan Kota", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis="y", labelsize=12)
    for index, value in enumerate(
        filtered_bystate_df.sort_values(by="customer_count", ascending=False)[
            "customer_count"
        ]
    ):
        ax.text(
            value + 0.5, index, f"{int(value)}", color="black", va="center", fontsize=10
        )
    plt.figtext(
        0.5,
        -0.05,
        f"Showing data above the 75th percentile or {percentile_75:.2f}",
        ha="center",
        fontsize=11,
        color="black",
    )

    # menampilkan grafik
    st.pyplot(plt.gcf())

with tab2:
    # judul untuk jumlah konsumen berdasarkan kota
    st.text("Customer Distribution by City")

    # menjalankan fungsi jumlah konsumen berdasarkan kota ke dalam variabel bycity_df
    bycity_df = create_bycity(main_data)

    # variabel untuk menandakan persentil 99.8 dari bycity_df
    percentile_998 = bycity_df["customer_count"].quantile(0.998)

    # hanya menampilkan data yang diatas atau sama dengan persentil 99.8
    filtered_bycity_df = bycity_df[bycity_df["customer_count"] >= percentile_998]

    # membuat ukuran figure untuk menyimpan grafik
    plt.figure(figsize=(12, 5))

    # menampilkan warna khusus untuk data pertama (jumlah terbanyak)
    colors_ = [
        "#72BCD4" if i == 0 else "#D3D3D3" for i in range(len(filtered_bycity_df))
    ]

    # menentukan x dan y dari bar chart
    ax = sns.barplot(
        x="customer_count",
        y="customer_city",
        data=filtered_bycity_df.sort_values(by="customer_count", ascending=False),
        palette=colors_,
    )

    # mengatur dan menampilkan informasi-informasi yang dibutuhkan
    plt.title("Number of Customer by States", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis="y", labelsize=12)
    for index, value in enumerate(
        filtered_bycity_df.sort_values(by="customer_count", ascending=False)[
            "customer_count"
        ]
    ):
        ax.text(
            value + 0.5, index, f"{int(value)}", color="black", va="center", fontsize=10
        )
    plt.figtext(
        0.5,
        -0.05,
        f"Showing data above the 99.8th percentile or {percentile_998:.2f}",
        ha="center",
        fontsize=11,
        color="black",
    )

    # menampilkan grafik
    st.pyplot(plt.gcf())

# subheader untuk review pelanggan
st.subheader("Hasil Review Pelanggan")

# menjalankan fungsi nilai review konsumen ke dalam variabel byreviewscore_df
byreviewscore_df = create_byreviewscore(main_data)

# menemukan nilai indeks dari row di dalam byreviewscore_df
max_value_index = byreviewscore_df["customer_count"].idxmax()

# membuat ukuran figure untuk menyimpan grafik
plt.figure(figsize=(10, 5))

# menampilkan warna khusus untuk data dengan jumlah terbanyak
colors_ = [
    "#72BCD4" if i == max_value_index else "#D3D3D3"
    for i in range(len(byreviewscore_df))
]

# menentukan x dan y dari bar chart
ax = sns.barplot(
    y="customer_count", x="review_score", data=byreviewscore_df, palette=colors_
)

# mengatur dan menampilkan informasi-informasi yang dibutuhkan
plt.title("Review Score Result", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis="x", labelsize=12)
for index, value in enumerate(byreviewscore_df["customer_count"]):
    ax.text(
        index, value + 0.5, f"{int(value)}", color="black", ha="center", fontsize=10
    )

# menampilkan grafik
st.pyplot(plt.gcf())
