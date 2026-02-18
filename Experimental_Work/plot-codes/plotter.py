import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from quadprog_fit import quadprog_fit
from matplotlib.colors import LinearSegmentedColormap
import scienceplots
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl


def plotter(model, group_variables,y0s,ind_variable_name,group_variable_name,automatic = True,max_idxs_manuel = [0,0,0,0],ind_variables = None):

    

    csv_file_path = f"csvs/{model}-{ind_variable_name}-{group_variable_name.lower()}.csv"
    df = pd.read_csv(csv_file_path)
    


    cmap = plt.colormaps["Set1"] #former: tab10
    cmap2 = plt.colormaps["Dark2"]
    markers = ["*","o","d","s","2","1"]
    markers2 = ["P","s","v","p","3"]



    line_fits = []
    x0s_all = np.zeros((len(y0s),len(group_variables)))

    group_variable_name_latex = rf"$\rm {group_variable_name[0]}_{group_variable_name[1]}$"
    mpl.rcParams['patch.linewidth'] = 0.3
    #LINFIT

    with plt.style.context(['science', 'ieee','no-latex','high-vis']):
        plt.rcParams.update({'axes.titlesize': 10,     # Başlık boyutu
                             'axes.labelsize': 10,     # Eksen etiket boyutu
                             'xtick.labelsize': 10,    # X ekseni tıklamalarının boyutu
                             'ytick.labelsize': 10,    # Y ekseni tıklamalarının boyutu
                             })

        fig, ax = plt.subplots()
        for idx, group_variable in enumerate(group_variables):

            if ind_variables is not None:
                df = df[df[ind_variable_name].isin(ind_variables)]
            df_ns = df[df[group_variable_name] == group_variable]
 

            layers = df_ns[ind_variable_name]
            accu_ts = df_ns["acc_tgt"]
            max_idx = np.argmax(accu_ts) if automatic else max_idxs_manuel[idx]
            
            layers1 = layers[max_idx:]
            accu_ts1 = accu_ts[max_idx:]

            line_fit = np.polyfit(layers1, accu_ts1,deg = 1)
            line_fits.append(line_fit)
            asdasda = np.linspace(min(layers1),max(layers1),1000)
            line_val = np.polyval(line_fit,asdasda) 

            ax.plot(layers, accu_ts,f"{markers2[idx]}", label = str(group_variable), color = cmap(idx)) # exp results
            ax.plot(asdasda,line_val,color = cmap(idx))
        

        ax.yaxis.set_major_locator(MaxNLocator(5))  # Set max 5 y-ticks
        ax.xaxis.set_major_locator(MaxNLocator(5))
        
        #ax.set_xlabel(f"{ind_variable_name}".capitalize())
        ax.set_xlabel(f"$L$" if ind_variable_name == "layer" else f"$d$")
        ax.set_ylabel("Target Accuracy")
        ax.legend(title = group_variable_name_latex,ncol = 2,fontsize = 8,title_fontsize = 9,frameon=True, facecolor='white',edgecolor='black',loc = "lower left") 
        plt.savefig(f'plots/{model}-{ind_variable_name}-{group_variable_name}-linefit.pdf',dpi = 600)
        plt.close()





    #QUADFIT
    with plt.style.context(['science', 'ieee','no-latex','high-vis']):
        plt.rcParams.update({'axes.titlesize': 10,     # Başlık boyutu
                        'axes.labelsize': 10,     # Eksen etiket boyutu
                        'xtick.labelsize': 10,    # X ekseni tıklamalarının boyutu
                        'ytick.labelsize': 10,    # Y ekseni tıklamalarının boyutu
                        })

        fig, ax = plt.subplots()
        for idx_y0, y0 in enumerate(y0s):

            for idx_ns,group_variable in enumerate(group_variables):
                line_fit = line_fits[idx_ns]
                x0 = (y0 - line_fit[1])/line_fit[0]
                x0s_all[idx_y0,idx_ns] = x0

            x0s = x0s_all[idx_y0,:]
            quad_fit, x0s_val, quad_val = quadprog_fit(x0s,group_variables)


            # Plot the quadratic fit curve
            ax.plot(x0s_val, quad_val, label=f'{y0:.2f}',color = cmap2(idx_y0))

            # Plot the data points
            ax.plot(x0s, group_variables, markers[idx_y0],color = cmap2(idx_y0))

        plt.rc('text', usetex=True)

        from matplotlib.ticker import ScalarFormatter
        formatter = ScalarFormatter()
        formatter.set_powerlimits((-3, 3))  # Bilimsel gösterim için limitleri ayarla
        ax.yaxis.set_major_formatter(formatter)

        ax.yaxis.set_major_locator(MaxNLocator(5))  # Set max 5 y-ticks
        ax.xaxis.set_major_locator(MaxNLocator(5))
        #ax.set_xlabel(f"{ind_variable_name}".capitalize())
        ax.set_xlabel(f"$L$" if ind_variable_name == "layer" else f"$d$")
        ax.set_ylabel(group_variable_name_latex)
        ax.legend(title="Target Accuracy",fontsize = 8,title_fontsize = 9,frameon=True, facecolor='white',edgecolor='black')


        plt.savefig(f"plots/{model}-{ind_variable_name}-{group_variable_name}-quadprog.pdf",dpi = 600)
        plt.close()
