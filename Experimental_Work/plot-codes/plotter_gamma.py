import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import argparse
from scipy.optimize import curve_fit
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator   

import scienceplots
plt.style.use(['science', 'ieee','no-latex','high-vis'])

def plotter_gamma(Mts,Mss,type):

        
    plt.rcParams.update({'axes.titlesize': 10,     # Başlık boyutu
                            'axes.labelsize': 10,     # Eksen etiket boyutu
                            'xtick.labelsize': 10,    # X ekseni tıklamalarının boyutu
                            'ytick.labelsize': 10,    # Y ekseni tıklamalarının boyutu
                            })

    ### inputs
    csv_path_name = f"csvs/{type}-opt.csv"
    ###


    df = pd.read_csv(csv_path_name)

    cmap = plt.colormaps["Set1"] #former: tab10
    cmap2 = plt.colormaps["Dark2"]    


    markers = ["*","o","d","s","2","1"]
    markers2 = ["P","s","v","p","3",1,2,3,"1","2","4",4]
    markers3 = ['o', 's', '^', '*', 'd']
    automatic = True
    max_idxs_manuel = [4,4,4,3]

    

    
    opt_gammas_list = np.zeros((len(Mss),len(Mts)))
    mpl.rcParams['patch.linewidth'] = 0.3

    for idx_Ms,Ms in enumerate(Mss):
        fig = plt.figure()
        quad_fits = []
        df_ms = df[df["Ms"] == Ms]
        for idx, Mt in enumerate(Mts):
            df_mt = df_ms[df_ms["Mt"] == Mt]


            gammas = df_mt["gamma"] if type == "adv" else df_mt["alpha"]

            accu_ts = df_mt["acc_tgt"]

            # max_idx = np.argmax(accu_ts) if automatic else max_idxs_manuel[idx]
            # gammas1 = gammas[max_idx:]
            # accu_ts1 = accu_ts[max_idx:]
            
            gammas1 = gammas
            #gammas1 = [0.1, 0.3, 0.5, 0.7, 0.9]
            
            accu_ts1 = accu_ts
            #accu_ts1 = [df_mt[df_mt["gamma"] == gamma]["accu_t_smoothed"].to_list()[0] for gamma in gammas1]

            
            # fig.suptitle('İlk Denemeler')
            

            quad_fit = np.polyfit(gammas1, accu_ts1,deg = 2)
            quad_fits.append(quad_fit)
            asdasda = np.linspace(min(gammas1),max(gammas1),1000)
            asdasda = np.linspace(0,1,1000)
            line_val = np.polyval(quad_fit,asdasda)



            plt.plot(gammas, accu_ts,f"{markers2[idx]}", label = str(Mt), color = cmap(idx)) # exp results 
            plt.plot(asdasda,line_val,color = cmap(idx))

            plt.gca().yaxis.set_major_locator(MaxNLocator(5))
            plt.gca().xaxis.set_major_locator(MaxNLocator(5))

            plt.xlabel(r"$\alpha$")
            plt.ylabel("Target Accuracy")
            plt.legend(title = r'$\rm M_t$',ncol=2,fontsize = 8,title_fontsize = 9,frameon=True, facecolor='white',edgecolor='black') 
            #plt.grid(True)
            #plt.ylim([0.5, 0.9])
            # plt.xlim([0, 1])
        
        plt.savefig(f'plots/{type}-optalpha-quadfit_Ms{Ms}.pdf')

        opt_gammas = [-quad_fit[1]/(2*quad_fit[0]) for quad_fit  in quad_fits]
        opt_gammas_list[idx_Ms,:] = opt_gammas

    # fig2 = plt.figure(figsize = (8,6))
    # plt.plot(Mts,opt_gammas)
    # plt.savefig('optgamma_vs_mt.pdf')
    # plt.grid(True)
    # plt.xlabel("Mt")
    # plt.ylabel("Optimum Gamma")
    
    fig3 = plt.figure()


    for idx_Ms, Ms in enumerate(Mss):
        x_data = Mts
        y_data = opt_gammas_list[idx_Ms]

        b,fitted_x,fitted_y = square_fit(x_data,y_data)

        plt.plot(x_data, y_data, f"{markers3[idx_Ms]}",color=cmap2(idx_Ms), label=f'{Ms}')
        plt.plot(fitted_x, fitted_y, color=cmap2(idx_Ms))

    plt.gca().yaxis.set_major_locator(MaxNLocator(5))
    plt.gca().xaxis.set_major_locator(MaxNLocator(5))
    plt.xlabel(r'$\rm M_t$')
    plt.ylabel(r'$\rm \alpha_{opt}$')
    #plt.title(r'$a\sqrt{x}$')
    plt.legend(title = r'$\rm M_s$',fontsize = 8,title_fontsize = 9,frameon=True, facecolor='white',edgecolor='black')
    #plt.grid(True)
    plt.savefig(f"plots/{type}-optalpha-asqrtx_fit_den_Mss.pdf")

def square_fit(x_data, y_data):
    # Define the model function
    def model(x, a, b):
        return a + b * np.sqrt(x)
    def model2(x, b):
        return b * np.sqrt(x)

    # Perform the curve fitting
    params, covariance = curve_fit(model2, x_data, y_data)

    # Extracting the parameters
    # a, b = params
    b = params
    # print("Fitted parameters: a =", a, "b =", b)
    

    # Generate y values based on the fitted model
    fitted_x = np.linspace(min(x_data),max(x_data),1000)
    # fitted_y = model(fitted_x, a, b)
    fitted_y = model2(fitted_x, b)

    return b, fitted_x, fitted_y