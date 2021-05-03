from numpy import fill_diagonal
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import regex as re
import time
"""
def cleantext(cadena):
    cadena=str(cadena)
    cadena.replace('\n',' ')
    cadena_limpia=[x.upper()  for x in cadena if (x.isalphanum() or x.isspace() or x=="'")]
    return ' '.join(''.join(cadena_limpia).split())
"""
def cleantext(cadena):
    pattern = r"[a-zA-Z0-9\'\s\.]"
    try:
        limpia = re.findall(pattern, cadena)
        limpia="".join(limpia).strip().upper()
        sin_dobles_espacios=re.sub(r'\s+'," ",limpia)
        sin_parentesis=re.sub(r"\(|\)","",sin_dobles_espacios)
        return sin_parentesis
    except:
        return []

def plotsongs(data):
    df = pd.DataFrame(data)
    df=df.set_index('title')
    labels = ['Compuesto', 'Positivo', 'Neutro', 'Negativo']
    colors = ["#1F8BDB", "#2BFC79","#FF9D2E", "#DB1F30"]

    df[['com','pos','neu','neg']].plot.bar(rot=0, color=colors)
    plt.title('Canciones')
    plt.subplot()
    plt.legend(labels, loc='upper right')
    plt.title("Ranking")
    plt.xticks(rotation=45)
    plt.tight_layout()

    new_graph_name = "salida" + str(time.time()) + ".png"
    plt.savefig("static/" + new_graph_name)
    plt.close()
    return new_graph_name

def plotartist(data):
    df = pd.DataFrame(data)
    labels = ['Negativo', 'Neutro',  'Positivo','Compuesto']
    colors = ["#1F8BDB", "#2BFC79","#FF9D2E", "#DB1F30"]
    sns.set_palette(sns.color_palette(colors))
    sns_plot=sns.histplot(data= df[['com','pos','neu','neg']], element="poly")
    sns_plot.legend(labels, loc='upper right')
    fig=sns_plot.get_figure()
    new_graph_name = "salida" + str(time.time()) + ".png"
    fig.savefig("static/" + new_graph_name)
    plt.close()
    return new_graph_name
