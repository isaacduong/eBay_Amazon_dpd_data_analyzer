import logging
import os
import re
import shutil
import subprocess
import sys
import time
import tkinter as tk
import warnings
from tkinter import *
from tkinter import ttk
from tkinter.constants import END, NORMAL

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

logging.basicConfig(level=logging.INFO)

german_stopwords = [
    "mann",
    "original",
    "neu",
    "holz",
    "finger",
    "hochglanz",
    "vorne",
    "liter",
    "hinten",
    "elektro",
    "kommode",
    "inkl",
    "benzin",
    "bar",
    "nass",
    "fein",
    "kopf",
    "for",
    "Satz",
    "Forum",
    "Garten",
    "passend",
    "BOX",
    "BIT",
    "GBA",
    "SDS",
    "GAL",
    "GSR",
    "PLUS",
    "GST",
    "GKS",
    "TPN",
    "EUR",
    "set",
    "neue",
    "alte",
    "Akku",
    "Watt",
    "GSA",
    "teilig",
    "aber",
    "alle",
    "allem",
    "allen",
    "aller",
    "alles",
    "als",
    "also",
    "am",
    "an",
    "ander",
    "andere",
    "anderem",
    "anderen",
    "anderer",
    "anderes",
    "anderm",
    "andern",
    "anderr",
    "anders",
    "auch",
    "auf",
    "aus",
    "bei",
    "bin",
    "bis",
    "bist",
    "da",
    "damit",
    "dann",
    "der",
    "den",
    "des",
    "dem",
    "die",
    "das",
    "dass",
    "da",
    "derselbe",
    "derselben",
    "denselben",
    "desselben",
    "demselben",
    "dieselbe",
    "dieselben",
    "dasselbe",
    "dazu",
    "dein",
    "deine",
    "deinem",
    "deinen",
    "deiner",
    "deines",
    "denn",
    "derer",
    "dessen",
    "dich",
    "dir",
    "du",
    "dies",
    "diese",
    "diesem",
    "diesen",
    "dieser",
    "dieses",
    "doch",
    "dort",
    "durch",
    "ein",
    "eine",
    "einem",
    "einen",
    "einer",
    "eines",
    "einig",
    "einige",
    "einigem",
    "einigen",
    "einiger",
    "einiges",
    "einmal",
    "er",
    "ihn",
    "ihm",
    "es",
    "etwas",
    "euer",
    "eure",
    "eurem",
    "euren",
    "eurer",
    "eures",
    "gegen",
    "gewesen",
    "hab",
    "habe",
    "haben",
    "hat",
    "hatte",
    "hatten",
    "hier",
    "hin",
    "hinter",
    "ich",
    "mich",
    "mir",
    "ihr",
    "ihre",
    "ihrem",
    "ihren",
    "ihrer",
    "ihres",
    "euch",
    "im",
    "in",
    "indem",
    "ins",
    "ist",
    "jede",
    "jedem",
    "jeden",
    "jeder",
    "jedes",
    "jene",
    "jenem",
    "jenen",
    "jener",
    "jenes",
    "jetzt",
    "kann",
    "kein",
    "keine",
    "keinem",
    "keinen",
    "keiner",
    "keines",
    "machen",
    "man",
    "manche",
    "manchem",
    "manchen",
    "mancher",
    "manches",
    "mein",
    "meine",
    "meinem",
    "meinen",
    "meiner",
    "meines",
    "mit",
    "muss",
    "musste",
    "nach",
    "nicht",
    "nichts",
    "noch",
    "nun",
    "nur",
    "ob",
    "oder",
    "ohne",
    "sehr",
    "sein",
    "seine",
    "seinem",
    "seinen",
    "seiner",
    "seines",
    "selbst",
    "sich",
    "sie",
    "ihnen",
    "sind",
    "so",
    "solche",
    "solchem",
    "solchen",
    "solcher",
    "solches",
    "soll",
    "sollte",
    "sondern",
    "sonst",
    "um",
    "und",
    "uns",
    "unsere",
    "unserem",
    "unseren",
    "unser",
    "unseres",
    "unter",
    "viel",
    "vom",
    "von",
    "vor",
    "war",
    "waren",
    "warst",
    "was",
    "weg",
    "weil",
    "weiter",
    "welche",
    "welchem",
    "welchen",
    "welcher",
    "welches",
    "wenn",
    "werde",
    "werden",
    "wie",
    "wieder",
    "will",
    "wir",
    "wird",
    "wirst",
    "wo",
    "wollen",
    "wollte",
    "zu",
    "zum",
    "zur",
    "zwar",
    "zwischen",
]

label_text_font = ("Courier", 25)
label_text_color = "white"
entry_text_font = ("Courier", 30)
entry_text_color = "#cc6d00"
bg_color = "lightgrey"
highlightbackground = "#cc6d00"


def click_shopname(event):
    shopname_entry.configure(state=NORMAL)
    shopname_entry.delete(0, END)
    shopname_entry.unbind("<Button-1>", clicked_shopname)


def click_email(event):
    email_entry.configure(state=NORMAL)
    email_entry.delete(0, END)
    email_entry.unbind("<Button-1>", clicked_email)


def click_num(event):
    num_bestsellers_entry.configure(state=NORMAL)
    num_bestsellers_entry.delete(0, END)
    num_bestsellers_entry.unbind("<Button-1>", clicked_num)


window = Tk()
window.resizable(False, False)
window.title("Made by ISAAC DUONG <3 ")
window.geometry("1000x700+200+100")

style = ttk.Style()

style.theme_use("clam")
style.configure(
    "TButton",
    background="grey",
    foreground="white",
    font=label_text_font,
    width=20,
    height=20,
    borderwidth=1,
    padx=5,
    pady=4,
    focusthickness=3,
    focuscolor="green",
)
style.map("TButton", background=[("active", "#cc6d00")])

xcor = 500
xcor_entry = xcor - 300
ycor = 150
dist = 130

c = Canvas(width=1000, height=750)
c.pack()

# the image
image = PhotoImage(file="bgimage.png")
c.create_image(0, 0, image=image)

c.create_text(xcor, 80, text="SALES ANALYZING TOOL", font=("Arial", 60, "bold"))

c.create_text(
    xcor,
    ycor + 0 * dist,
    text="den Shop-Namen eingeben",
    font=label_text_font,
    fill=label_text_color,
)

c.create_text(
    xcor,
    ycor + 1 * dist,
    text="Anzahl meistverkaufter Produkte",
    font=label_text_font,
    fill=label_text_color,
)

c.create_text(
    xcor,
    ycor + 2 * dist,
    text="Bericht wird an foldende eMailadresse gesendet",
    font=label_text_font,
    fill=label_text_color,
)

shopname_entry = Entry(
    c,
    width=30,
    font=entry_text_font,
    foreground=entry_text_color,
    highlightbackground=highlightbackground,
    highlightthickness=2,
    justify="center",
)
shopname_entry.insert(0, "coldmooncosmetics")
shopname_entry.place(x=xcor_entry, y=ycor + 0.2 * dist)
clicked_shopname = shopname_entry.bind("<Button-1>", click_shopname)


num_bestsellers_entry = Entry(
    c,
    width=30,
    font=entry_text_font,
    foreground=entry_text_color,
    highlightbackground=highlightbackground,
    highlightthickness=2,
    justify="center",
)
num_bestsellers_entry.insert(0, "20")
num_bestsellers_entry.place(x=xcor_entry, y=ycor + 1.2 * dist)
clicked_num = num_bestsellers_entry.bind("<Button-1>", click_num)


email_entry = Entry(
    c,
    width=30,
    font=entry_text_font,
    foreground=entry_text_color,
    highlightbackground=highlightbackground,
    highlightthickness=2,
    justify="center",
)
email_entry.insert(0, "isaaacduong@gmail.com")
email_entry.place(x=xcor_entry, y=ycor + 2.2 * dist)
clicked_email = email_entry.bind("<Button-1>", click_email)

################################################################


def call():
    start_time = time.time()
    logging.info("calling function")
    shop_name = shopname_entry.get()
    num_bestsellers = int(num_bestsellers_entry.get())
    emails = email_entry.get()
    real_sales = True
    ebay_real_sales = 3
    amazon_realsales = 10
    shop_category = "Technik"

    if emails:
        password = "!Elirmb33oG"  # input('Password eingeben: ') #'!El***33oG'

    # In[9]:

    pd.set_option(
        "display.float_format", lambda x: "%.0f" % x
    )  # show only decimal number

    warnings.filterwarnings("ignore")

    plt.style.use("fivethirtyeight")
    plt.rcParams["grid.color"] = (0.9, 0.9, 0.9, 0.1)

    # In[10]:

    if shop_category == "Haushalt":
        xytext_x = 200
    elif shop_category == "Werkzeug":
        xytext_x = 500
    elif shop_category == "Technik":
        xytext_x = 300
    else:
        xytext_x = 400

    categories = {
        "Werkzeug": {"bins": 150, "y_max_rate": 0.2, "x_max_rate": 3},
        "Technik": {"bins": 250, "y_max_rate": 0.1, "x_max_rate": 3},
        "Haushalt": {"bins": 250, "y_max_rate": 0.5, "x_max_rate": 5},
    }

    # In[11]:

    names = {
        "card__item": "Artikelname",
        "card__price": "Artikelpreis",
        "tablescraper-selected-row": "Zeitraum",
        "card__item 2": "Artikelnummer",
        "card__item href": "Artikel_link",
    }

    # In[12]:

    df6 = pd.read_csv(
        f"./{shop_name}6.csv",
        usecols=[
            "card__item",
            "card__item 2",
            "card__item href",
            "card__price",
            "tablescraper-selected-row",
        ],
    )
    df6.rename(names, inplace=True, axis=1)
    df6 = df6.loc[
        df6["Zeitraum"].isin(["Letzter Monat", "Letzte 6 Monate"]), :
    ]  # last six month data

    # In[13]:

    df6_12 = pd.read_csv(
        f"./{shop_name}12.csv",
        usecols=["card__item", "card__price", "tablescraper-selected-row"],
    )

    # create columns as in table last six months
    df6_12["card__item href"] = np.nan
    # create columns as in table last six months
    df6_12["card__item 2"] = np.nan
    df6_12.rename(names, inplace=True, axis=1)
    # six months before last six months
    df6_12 = df6_12.loc[df6_12["Zeitraum"] == "Letztes Jahr", :]

    # In[14]:

    # concatenate to full data
    df = pd.concat([df6, df6_12], ignore_index=True)

    def short_item_name(text, words=3):

        # pattern = r'\b\w+\b'  # pattern to find words
        pattern = r"\b[a-zA-Z]{3,20}\b"
        match = re.findall(pattern, text)
        text = " ".join(match[:words])  # show only some words
        return text

    # In[17]:

    def convert_datatype(df):

        df["Preis_EUR"] = df.Artikelpreis.str.split(expand=True)[1]  # remove EUR
        df["Preis_EUR"] = df.Preis_EUR.str.replace(".", "")
        df["Preis_EUR"] = df.Preis_EUR.str.replace("$", "")
        df["Preis_EUR"] = df.Preis_EUR.str.replace(",", ".")
        df["Preis_EUR"] = df.Preis_EUR.astype(float)
        df.drop("Artikelpreis", inplace=True, axis=1)
        return df

    # In[18]:

    def split_number(text):

        match = re.search(r"[0-9]{12}", str(text))
        return match.group() if match else None

    # In[19]:

    def remove_item_number(text):
        """ function to remove item number from description"""
        text = str(text)
        pattern1 = r"[0-9]{12}"
        pattern2 = r"\(Nr\."
        text = re.sub(r"\)", "", text)  # remove ')'
        text = re.sub(pattern1, "", text)  # remove item number
        text = re.sub(pattern2, "", text)  # remove (Nr .

        return text

    # In[20]:

    def fill_nan(df):

        df["Artikelnummer_temp"] = df["Artikelname"].apply(split_number)
        nan_index = df[df["Artikelnummer"].isnull()].index
        df.loc[nan_index, "Artikelnummer"] = df.loc[
            nan_index, "Artikelnummer_temp"
        ]  # fill item number
        df.loc[nan_index, "Artikel_link"] = (
            "https://www.ebay.de/itm/" + df.loc[nan_index, "Artikelnummer"]
        )  # fill links
        df.drop("Artikelnummer_temp", axis=1, inplace=True)
        df.dropna(inplace=True)

        return df

    # In[21]:

    def format_table(df):

        df = convert_datatype(df)
        df = fill_nan(df)  # fill nan value in item number and item link column
        # remove item number from item description
        df["Artikelname"] = df["Artikelname"].apply(remove_item_number)
        df.Artikelnummer = df.Artikelnummer.astype(
            int
        )  # convert item number to type int

        return df

    # In[22]:

    def create_best_sellers(df, count):

        letzter_monat = df.loc[
            df["Zeitraum"].isin(["Letzter Monat"]), "Artikel_link"
        ].value_counts()
        letzte_6_monate = df.loc[
            df["Zeitraum"].isin(["Letzte 6 Monate"]), "Artikel_link"
        ].value_counts()
        letzte_6_12_monate = df.loc[
            df["Zeitraum"].isin(["Letztes Jahr"]), "Artikel_link"
        ].value_counts()

        best_sellers = pd.concat(
            [letzter_monat, letzte_6_monate, letzte_6_12_monate], axis=1
        )
        best_sellers.columns.values[0] = "Verkäufe letztes Monats in Stück"
        best_sellers.columns.values[1] = "Verkäufe letzter 6 Monate in Stück"
        best_sellers.columns.values[2] = "Verkäufe letzter 12 Monate in Stück"

        best_sellers["Durchschnittliche Verkäufe letzter 6 Monate"] = (
            best_sellers["Verkäufe letzter 6 Monate in Stück"] / 5
        )
        best_sellers["Durchschnittliche Verkäufe letzter 12 Monate"] = (
            best_sellers["Verkäufe letzter 12 Monate in Stück"] / 6
        )
        best_sellers["Durchschnittliche Verkäufe letzter 12 Monate"] = (
            best_sellers["Verkäufe letzter 6 Monate in Stück"]
            + best_sellers["Verkäufe letzter 12 Monate in Stück"]
        ) / 11

        best_sellers = best_sellers.iloc[:count, :]

        best_sellers = best_sellers.reset_index().merge(
            df.loc[:, ["Artikelname", "Artikel_link", "Preis_EUR"]]
            .drop_duplicates()
            .set_index("Artikel_link"),
            left_on="index",
            right_on="Artikel_link",
        )
        best_sellers_index = best_sellers["index"].drop_duplicates().index
        return best_sellers.loc[best_sellers_index, :].reset_index(drop=True)

    # In[23]:

    def create_revenue_columns(df):

        df["Umsatz/Monat"] = df["Verkäufe letztes Monats in Stück"] * df["Preis_EUR"]
        df["Umsatz/6_Monate"] = (
            df["Durchschnittliche Verkäufe letzter 6 Monate"] * 5 * df["Preis_EUR"]
            + df["Umsatz/Monat"]
        )
        df["Umsatz/12_Monate"] = (
            df["Durchschnittliche Verkäufe letzter 12 Monate"] * 11 * df["Preis_EUR"]
            + df["Umsatz/Monat"]
        )
        return df

    # In[24]:

    def change_datatype_to_int(df):

        df.fillna(0, inplace=True)
        columns = [
            "Verkäufe letztes Monats in Stück",
            "Durchschnittliche Verkäufe letzter 6 Monate",
            "Durchschnittliche Verkäufe letzter 12 Monate",
            "Umsatz/Monat",
            "Umsatz/6_Monate",
            "Umsatz/12_Monate",
        ]
        for column in columns:
            df[column] = df[column].round().astype(int)
        return df

    # In[25]:

    def write_to_file(df):
        logging.info(
            f"...csv-Datei wird erzeugt\n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        global path
        path = f"Verkaufsanalyse_{shop_name}"
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        change_datatype_to_int(df)
        df = df.rename(columns={"index": "Art_Link"})
        df = df.loc[
            :,
            [
                "Artikelname",
                "Preis_EUR",
                "Verkäufe letztes Monats in Stück",
                "Durchschnittliche Verkäufe letzter 6 Monate",
                "Durchschnittliche Verkäufe letzter 12 Monate",
                "Umsatz/Monat",
                "Umsatz/6_Monate",
                "Umsatz/12_Monate",
                "Art_Link",
            ],
        ]
        df.to_csv(f"{path}/{shop_name}_{num_bestsellers}_bestsellers.csv")

        return df

    def create_corpus(df):
        corpus = []

        for x in df["Artikelname"].str.split():
            for i in x:
                corpus.append(i)
        return corpus

    # In[26]:

    formated_table = format_table(df)
    best_sellers = create_best_sellers(formated_table, num_bestsellers)
    best_200 = create_best_sellers(formated_table, 200)
    final_df = create_revenue_columns(best_sellers)
    final_df = write_to_file(final_df)
    final_df["Art_Name"] = final_df.Artikelname.apply(short_item_name)

    # In[27]:
    def plot_monthly_sales(df, true_sales=True):

        bestsellers = df.loc[
            df["Zeitraum"] == "Letzter Monat", "Artikelname"
        ].value_counts()[:num_bestsellers]

        bestsellers = bestsellers * 4 if true_sales else bestsellers
        ax = bestsellers.plot(
            kind="barh", figsize=(16, 15), color="#0bff01", width=0.7, edgecolor="black"
        )
        plt.tick_params(
            axis="both",  # changes apply to the x and y-axis
            which="both",  # both major and minor ticks are affected
            right=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
        )
        ax.text(
            0.55,
            0.95,
            "Verkaufsmenge letztes Monats",
            fontdict={"fontsize": 20, "fontweight": "bold"},
            transform=ax.transAxes,
            bbox=dict(facecolor="#0bff01", alpha=0.5),
        )

        plt.savefig(f"{path}/Verkaufsmenge letztes Monates(1).pdf", bbox_inches="tight")
        logging.info(
            f"...Säulendiagramm monatlicher meistverkaufter Produkten gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )

    plot_monthly_sales(df, true_sales=real_sales)

    def plot_yearly_sales(df, true_sales=True):

        bestsellers = df.loc[:, ["Artikelname", "Preis_EUR"]].value_counts()[
            :num_bestsellers
        ]
        bestsellers = 4 * bestsellers if true_sales else bestsellers
        ax = bestsellers.plot(
            kind="barh",
            figsize=(15, 15),
            color="#fdfe02",
            width=0.7,
            edgecolor="black",
        )
        plt.tick_params(
            axis="both", which="both", right=False, top=False,
        )
        ax.text(
            0.55,
            0.95,
            "Verkaufsmenge letztes Jahres",
            fontdict={"fontsize": 20, "fontweight": "bold"},
            transform=ax.transAxes,
            bbox=dict(facecolor="#fdfe02", alpha=0.5),
        )
        plt.savefig(f"{path}/Verkaufsmenge letztes Jahres().pdf", bbox_inches="tight")

    # plot_yearly_sales(df, true_sales=real_sales)

    def comparedplot(df, true_sales=True):

        bestsellers = df.set_index("Artikelname").loc[
            :,
            [
                "Verkäufe letztes Monats in Stück",
                "Durchschnittliche Verkäufe letzter 6 Monate",
                "Durchschnittliche Verkäufe letzter 12 Monate",
            ],
        ]
        bestsellers = bestsellers * 4 if true_sales else bestsellers
        ax = bestsellers.plot(
            kind="barh",
            figsize=(15, 30),
            color=["#0bff01", "#fe0000", "#fdfe02"],
            edgecolor="black",
            width=0.9,
            alpha=0.8,
        )

        plt.savefig(f"{path}/Verkaufsanzahlvergleich(3).pdf", bbox_inches="tight")

    def trend_comparedplot(df, true_sales=True):
        logging.info(
            f"...Säulenvergleichdiagramm meistverkaufter Produkten wird gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        bestsellers = df.set_index("Artikelname").loc[
            :,
            [
                "Verkäufe letztes Monats in Stück",
                "Durchschnittliche Verkäufe letzter 6 Monate",
                "Durchschnittliche Verkäufe letzter 12 Monate",
            ],
        ]
        bestsellers = bestsellers * 4 if true_sales else bestsellers
        ax = bestsellers.plot(
            kind="barh",
            figsize=(15, 30),
            color=["#0bff01", "#fe0000", "#fdfe02"],
            edgecolor="black",
            width=0.9,
            alpha=0.3,
        )

        for i in range(len(df.index)):
            color1 = "g" if (df.iloc[i, 3] / 2 > df.iloc[i, 4] / 2) else "r"
            color2 = "g" if (df.iloc[i, 2] / 2 > df.iloc[i, 3] / 2) else "r"
            if true_sales:
                ax.annotate(
                    "",
                    xy=(df.iloc[i, 3] * 2, df.index[i]),
                    xytext=(df.iloc[i, 4] * 2, df.index[i] + 0.3),
                    arrowprops=dict(
                        color=color1,
                        arrowstyle="-",
                        # width=1
                    ),
                )
                ax.annotate(
                    "",
                    xy=(df.iloc[i, 2] * 2, df.index[i] - 0.3),
                    xytext=(df.iloc[i, 3] * 2, df.index[i]),
                    arrowprops=dict(
                        color=color2,
                        # arrowstyle='->',
                        width=1,
                    ),
                )
            else:
                ax.annotate(
                    "",
                    xy=(df.iloc[i, 3] / 2, df.index[i]),
                    xytext=(df.iloc[i, 4] / 2, df.index[i] + 0.3),
                    arrowprops=dict(
                        color=color1,
                        arrowstyle="-",
                        # width=1
                    ),
                )
                ax.annotate(
                    "",
                    xy=(df.iloc[i, 2] / 2, df.index[i] - 0.3),
                    xytext=(df.iloc[i, 3] / 2, df.index[i]),
                    arrowprops=dict(
                        color=color2,
                        # arrowstyle='->',
                        width=1,
                    ),
                )
        ax.text(0.7, 0.94, " --->", transform=ax.transAxes, color="g", fontsize=18)
        ax.text(0.76, 0.94, " Nachfrage steigt", transform=ax.transAxes, fontsize=15)
        ax.text(0.7, 0.92, " --->", transform=ax.transAxes, color="r", fontsize=18)
        ax.text(0.76, 0.92, " Nachfrage sinkt", transform=ax.transAxes, fontsize=15)

        plt.savefig(f"{path}/Verkaufstrend(3).pdf", bbox_inches="tight")

    def create_corpus(df):
        corpus = []

        for x in df["Artikelname"].str.split():
            for i in x:
                corpus.append(i)
        return corpus

    def plot_bestbrands(df, true_sales=True):

        logging.info(
            f"...Säulendiagramm meistverkaufter Produkten pro Monat wird gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        from matplotlib.ticker import FormatStrFormatter, MultipleLocator

        global german_stopwords
        german_stopwords = [word.upper() for word in german_stopwords]
        df.Artikelname = df.Artikelname.apply(short_item_name, 10)
        corpus = create_corpus(df)
        corpus = [word.upper() for word in corpus]
        words_series = pd.Series(corpus)
        words_series = words_series.value_counts(ascending=False)[:]
        words_series.drop(labels=german_stopwords, errors="ignore", inplace=True)
        mostfrequent_words = words_series.head(30)
        most_revenues = {}
        for i in range(len(mostfrequent_words)):

            product = mostfrequent_words.index[i]
            total = df.loc[
                df.Artikelname.str.upper().str.contains(product), "Preis_EUR"
            ].sum()
            most_revenues[product] = round(total)

        most_revenue_brands = pd.DataFrame(
            most_revenues.items(), columns=["Marke/Produkt", "Total_Verkaufsumme"]
        )
        most_revenue_brands["Total_Verkaufsumme"] = (
            4 * most_revenue_brands["Total_Verkaufsumme"]
            if true_sales
            else most_revenue_brands["Total_Verkaufsumme"]
        )

        fig, ax = plt.subplots(1, 1, figsize=(25, 12))
        ax = sns.barplot(
            data=most_revenue_brands, y="Total_Verkaufsumme", x="Marke/Produkt"
        )
        ax.set_xlabel("Marke/Produkt", fontdict={"fontsize": 16, "fontweight": "bold"})
        ax.set_ylabel("Umsatz in EUR", fontdict={"fontsize": 16, "fontweight": "bold"})
        ax.set_xticklabels(
            most_revenue_brands["Marke/Produkt"], rotation=30, ha="right"
        )
        ax.set_title(
            "Umsatz je Marke/Produkt pro Jahr",
            fontdict={"fontsize": 25, "fontweight": "bold"},
        )
        ax.yaxis.set_major_formatter(FormatStrFormatter("%d"))
        ax.yaxis.grid()
        ax.set_facecolor("grey")

        plt.savefig(
            f"{path}/Umsatz je Marke-Produkt pro Jahr(5).pdf", bbox_inches="tight"
        )

    plot_bestbrands(df, true_sales=real_sales)

    def plot_turnover_volume(df, num=25, true_sales=True):
        logging.info(
            f"...Säulenvergleichdiagramm von Umsatz meistverkaufter Produkten wird gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        fig, ax = plt.subplots(1, 1, figsize=(20, 12))
        df["Umsatz/Monat"] = (
            4 * df["Umsatz/Monat"] if true_sales else df["Umsatz/Monat"]
        )
        ax = sns.barplot(data=df, y="Umsatz/Monat", x="Artikelname")
        ax.set_xlabel(
            "Umsatzstarke Produkte", fontdict={"fontsize": 16, "fontweight": "bold"}
        )
        ax.set_ylabel(
            "Umsatz pro Monat in EUR", fontdict={"fontsize": 16, "fontweight": "bold"}
        )
        ax.set_xticklabels(df.Artikelname, rotation=30, ha="right")
        ax.set_title(
            "Umsatz je Produkt pro Monat",
            fontdict={"fontsize": 25, "fontweight": "bold"},
        )
        ax.yaxis.grid(True)
        ax.set_facecolor("grey")

        plt.savefig(f"{path}/Umsatz je Produkt pro Monat(4).pdf", bbox_inches="tight")

        # In[32]:

    def plot_product_revenue(df, num=25):
        logging.info(
            f"...Kreisdiagramm meistverkaufter Produkten wird gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))
        explode = np.zeros(num)
        explode[0] = 0.1
        labels = df.sort_values("Umsatz/12_Monate", ascending=False)[:num].Art_Name
        ax.pie(
            df["Umsatz/12_Monate"].sort_values(ascending=False)[:num],
            labels=labels,
            # shadow=True,
            radius=1.2,
            explode=explode,
            autopct="%1.1f%%",
            textprops={"fontsize": 16, "color": "black"},
            wedgeprops={"alpha": 0.9, "linewidth": 3},
        )
        ax.set_title(
            "Prozentualer Anteil am Verkauf",
            loc="center",
            fontdict={"fontsize": 30, "color": "black"},
        )

        plt.savefig(
            f"{path}/prozentualer Anteil am Verkauf(2).pdf", bbox_inches="tight"
        )

    plot_product_revenue(final_df, num=num_bestsellers)
    # In[33]:

    def plot_boxplot(df):

        plt.style.use("classic")
        fig, ax = plt.subplots(1, 1, figsize=(27.5, 12))
        ax = sns.boxplot(data=df, x="Preis_EUR", color="#0bff01")

        quantile_1 = round(df.Preis_EUR.quantile(0.25))
        quantile_3 = round(df.Preis_EUR.quantile(0.75))

        ax.set_xticks(range(0, round(df.Preis_EUR.max() / 100) * 100, 50))
        ax.annotate(
            f"50% des Umsatzes erzielt durch Verkauf von Produkten zw. {quantile_1} - {quantile_3} EUR ",
            xy=(quantile_3, 0.4),
            xytext=(500, 0.45),
            fontsize=20,
            arrowprops=dict(facecolor="red", shrink=0.05),
        )
        plt.xticks(rotation=90)
        plt.tick_params(
            axis="x", which="both", top=False,
        )
        plt.savefig(
            f"{path}/Preisspanne die 50% Umsatz generiert(7).pdf", bbox_inches="tight"
        )

    # In[41]:

    def plot_price_distribution(df, bins=200, x=500, y=10000):

        logging.info(
            f"...Histogram(Verteilung der Verkaufspreis) wird gezeichnet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        plt.style.use("dark_background")
        fig, ax = plt.subplots(1, 1, figsize=(22, 12))
        ax.hist(df.Preis_EUR, bins=bins, color="#0bff01", alpha=0.8, lw=3)
        ax.set_title(
            f"Gesamtumsatz von {shop_name}",
            fontdict={"family": "serif", "weight": "normal", "size": 30,},
        )
        ax.set_xlim(0, x)
        ax.set_xticks(range(0, x, int(x / 20)))
        ax.set_xlabel("Preisspanne in EUR", fontweight="bold", fontsize=15)

        ax.set_ylim(0, y)
        ax.set_yticks(range(0, y, int(y / 20)))
        ax.set_ylabel("Anzahl verkaufter Produkte", fontweight="bold", fontsize=15)

        ax.text(
            x / 3,
            6 * y / 7,
            f"  eBay ca. {round(df.Preis_EUR.sum()*4/1000000,2) } Mio EUR                         \n Amazon ca. {round(df.Preis_EUR.sum()*60/1000000,2) } Mio EUR",
            fontdict={
                "family": "serif",
                "color": "red",
                # 'weight': 'normal',
                "size": 30,
                "fontweight": "bold",
            },
        )
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        plt.grid(False)
        plt.tick_params(
            axis="both",  # changes apply to the x and y-axis
            which="both",  # both major and minor ticks are affected
            right=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            # labelbottom=False
        )
        plt.tight_layout()
        plt.savefig(f"{path}/Gesamtumsatz(6).pdf", bbox_inches="tight")
        plt.style.use("classic")

    # In[43]:

    # 'Werkzeug':{'bins':200,'y_max_rate':0.2,'x_max_rate':3},
    # 'Technik':{'bins':200,'y_max_rate':0.1,'x_max_rate':3},
    # 'Haushalt':{'bins':250,'y_max_rate':0.5,'x_max_rate':5},

    # comparedplot(final_df, true_sales=real_sales)
    trend_comparedplot(final_df, true_sales=real_sales)
    plot_turnover_volume(final_df, num_bestsellers, true_sales=real_sales)
    # plot_product_revenue(final_df, num_bestsellers)

    plot_boxplot(df)

    bins = categories[shop_category]["bins"]
    x_max = df.Preis_EUR.max() / categories[shop_category]["x_max_rate"]
    y_max = categories[shop_category]["y_max_rate"] * bins ** 2
    plot_price_distribution(df, bins=bins, y=round(y_max), x=round(x_max))

    # In[44]:

    def merge_pdfs(source_dir, shop=""):

        from PyPDF2 import PdfFileMerger

        merger = PdfFileMerger()
        files = os.listdir(source_dir)
        pdfs = [
            file
            for i in range(len(files))
            for file in files
            if ("(" + str(i + 1) + ")") in file and file.endswith("pdf")
        ]
        for pdf in pdfs:
            # if pdf.endswith('pdf'):
            merger.append(source_dir + "/" + pdf)

        merger.write(source_dir + f"/Verkaufsanalyse_von_{shop}.pdf")
        logging.info(
            f"...Dateien werden zusammengefügt \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        merger.close()

    def send_email_with_attachment(
        password,
        receiver,
        files=[],
        server="smtp.gmail.com",
        port=587,
        use_tls=True,
        shop="",
    ):

        import smtplib
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.utils import COMMASPACE, formatdate
        from pathlib import Path

        send_from = "isaaacduong@gmail.com"
        msg = MIMEMultipart()
        msg["From"] = send_from
        # msg['To'] = COMMASPACE.join(send_to)
        # msg['To'] = send_to

        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = f"Verkaufsanalyse"
        message = (
            f"Hallo, hier ist nochmals die Verkaufsanalyse von dem ebay shop {shop}\n\n"
        )

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase("application", "octet-stream")
            with open(path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", "attachment; filename={}".format(Path(path).name)
            )
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(send_from, password)

        smtp.sendmail(send_from, receiver, msg.as_string())
        logging.info(
            f"...email wird an {receiver} gesendet \n Programmdauer in Sek -->>>{round(time.time()-start_time)}<<<-- "
        )
        smtp.quit()

    # In[47]:

    merge_pdfs(path, shop_name)

    if sys.platform:

        subprocess.Popen(
            ["open", f"{path}/{shop_name}_{num_bestsellers}_bestsellers.csv"]
        )
        time.sleep(1)
        subprocess.Popen(["open", f"{path}/Verkaufsanalyse_von_{shop_name}.pdf"])

    if emails:
        files = [
            f"Verkaufsanalyse_von_{shop_name}.pdf",
            f"{shop_name}_{num_bestsellers}_bestsellers.csv",
        ]
        files_paths = [path + "/" + file for file in files]
        send_email_with_attachment(
            password, receiver=emails, files=files_paths, shop=shop_name
        )

    # In[48]:

    window.destroy()


button = ttk.Button(c, text="BERICHT ERSTELLEN", command=call)
# button.bind('<Enter>', call)
button.place(x=xcor - 170, y=ycor + 3 * dist)
window.mainloop()
