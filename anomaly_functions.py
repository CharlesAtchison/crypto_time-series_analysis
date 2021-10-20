import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def generateBollingerBands(df, k=2, ema_lst=[7, 14, 30, 60, 90]):
    '''Pass df with index that's DateTimeIndex and only one continuious column
    '''
    
    result = ''
    col_name = df.columns[0]
    # list of each dataframe that contains the bollinger_bands
    bollinger_df_dict = dict()
    
    def plotFigure(my_df, ema, col_name):
            plt.figure(figsize=(16,8))
            tmp_result = ''
            plt.plot(my_df.index, my_df.rate, label=col_name.title())
            plt.plot(my_df.index, my_df.midband, label=f'{ema}-day EMA/Midband')
            plt.plot(my_df.index, my_df.upper_band, label='Upper Band')
            plt.plot(my_df.index, my_df.lower_band, label='Lower Band')
            plt.legend(loc='best')
            plt.ylabel(col_name.title())
            plt.title(f'{ema} Day Bollinger Band for {col_name.title()}')
            figname = f'images/{ema}_day_bb_plot.png'
            tmp_result += f'#### {ema}-Day Bollinger Band Plot\n\n'
            tmp_result += f"![{ema}_day_bb_{col_name}_plt]({figname} '{ema}_day_bb_{col_name}_image')\n\n"
            if not os.path.exists('images'):
                os.makedirs('images')
                print('Created Directory images')
            plt.savefig(figname)
            plt.show()
            return tmp_result

    for ema in ema_lst: 
        # Calculate Midband
        midband = df.ewm(span=ema).mean()
        stdev = df.ewm(span=ema).std()
        upper_band = midband + stdev * k
        lower_band = midband - stdev * k
        bollinger_band = pd.concat([upper_band, lower_band], axis=1)
        bollinger_band.columns = ['upper_band', 'lower_band']
        my_df = pd.concat([df, midband, bollinger_band], axis=1)
        my_df.columns = [col_name, 'midband', 'upper_band', 'lower_band']
        
        # Add to the markdown result
        result += plotFigure(my_df, ema, col_name)

        # Calculate the %b for the respective dataframe and current time period
        my_df['pct_b'] = (my_df[col_name] - my_df.lower_band) / (my_df.upper_band - my_df.lower_band)
        bollinger_df_dict[f'{ema}_day'] = my_df

    return bollinger_df_dict, result


def generateEMA(df, ema_lst = [7, 14, 30, 60, 90]):

    plt.figure(figsize=(16, 8))

    plt.plot(df.index, df, label=f'Daily', alpha=.5)
    for ema in ema_lst:
        ## Plot the Exponential Moving Average 
        # Plot the midband
        midband = df.ewm(span=ema).mean()
        plt.plot(df.index, midband, label=f'{ema}-day EMA')
        plt.legend(loc='best')
        plt.title('EMA')
    plt.show()