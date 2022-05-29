# from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import plotly.express as px
# from .models import car
import plotly.io as pio
pio.renderers.default = "svg"
from operator import itemgetter
from plotly.offline import download_plotlyjs,plot

# READING FROM SQLITE DATABASE *************

df = pd.read_sql_table('graph_car', 'sqlite:///D:\MY CODES\Django\graph\db.sqlite3')
df.convert_dtypes().dtypes

df.Price*=1000
df.Sales2022*=1000
df.Sales2021*=1000
df['Tags']=df['Make']+' '+df['Model']+' '+df['Variant']
df['Mileage'] = df['Mileage'].str.rstrip(" km/litre" or ' km/ltr')
df['Mileage']=df['Mileage'].astype('float32')
df["Displacement"] = df["Displacement"].str.rstrip(" cc" or 'cc')
cs2=df[['Displacement']].dropna(how='any')
cs2['Displacement']=cs2['Displacement'].astype('int32')
df["Ground_Clearance"] = df["Ground_Clearance"].str.rstrip(" mm" or 'mm')

tsales22=df['Sales2022'].sum()
tsales22=int(tsales22)
tsales21=df['Sales2021'].sum()
tsales21=int(tsales21)


   # BRAND and INFO      ************************

brandsale22df=df.groupby('Make')[['Sales2022','Sales2021']].sum().sort_values('Sales2022',ascending=False)
bs1=brandsale22df['Sales2022']-brandsale22df['Sales2021']
x3=bs1*100/brandsale22df['Sales2021']
x3=round(x3,2)
brandsale22=pd.DataFrame({
   'S. No.':[i for i in range(1,len(brandsale22df.index)+1)],
   'Car brand':brandsale22df.index,
   'Total Sales 2022':brandsale22df['Sales2022'].astype('int32'),
   'Total Sales 2021':brandsale22df['Sales2021'].astype('int32'),
   'Growth rate (%)':x3
})
x3=brandsale22df['Sales2022']*100/tsales22
x3=round(x3,2)
brandsale22['Market share 2022 (%)']=x3




def home(req):
   
   # CARDS CALCULATION *******************************************************

   brandsale22html=brandsale22.to_html(classes='table table-borderless',justify='unset',index=False)
   arg={
      'makesales22':brandsale22html,
      'tsales22':tsales22
   }
   arg['tsales21']=tsales21

   x1=(tsales22-tsales21)*100/tsales21
   arg['growthrate']=round(x1,3)

   x1=df['Price'][df.Price==df.Price.max()].to_numpy()
   x1=int(x1[0])
   arg['eprice']=x1
   x1=df['Price'][df.Price==df.Price.min()].to_numpy()
   x1=int(x1[0])
   arg['cprice']=x1
   x1=df['Sales2022'][df.Sales2022==df.Sales2022.max()].to_numpy()
   x1=int(x1[0])
   arg['esl22']=x1
   x1=df['Sales2022'][df.Sales2022==df.Sales2022.max()].to_numpy()
   x1=int(x1[0])
   arg['csl22']=x1
   x1=df['Sales2021'][df.Sales2021==df.Sales2021.max()].to_numpy()
   x1=int(x1[0])
   arg['esl21']=x1
   x1=df['Sales2021'][df.Sales2021==df.Sales2021.max()].to_numpy()
   x1=int(x1[0])
   arg['csl21']=x1
   x1=cs2.Displacement[cs2.Displacement==cs2.Displacement.max()].to_numpy()
   x1=x1[0]
   arg['hdis']=x1
   x1=cs2.Displacement[cs2.Displacement==cs2.Displacement.min()].to_numpy()
   x1=x1[0]
   arg['ldis']=x1

   x2=[]
   bs6,bs4,bs3=0,0,0
   for i in df.Emission_Norm:
      if i =='BS 6':
         bs6+=1
      elif i == 'BS IV':
         bs4+=1
      elif i == 'BS III':
         bs3+=1
   x2=[[bs6,'BS VI'],[bs4,'BS IV'], [bs3,'BS III']]
   x2=sorted(x2, key=itemgetter(0), reverse=True)
   arg['bs']=x2
   x3=[]
   x1=x2[0][0] +x2[1][0]+x2[2][0]
   x3.append(round(x2[0][0]*100/x1,2))
   x3.append(round(x2[1][0]*100/x1,2))
   x3.append(round(x2[2][0]*100/x1,2))
   arg['bs1']=x3



# FINDING POPULAR ATTRIBUTES BY SALES 2022  #########

   class sales22:
      def __init__(self,a,b) :
         self.a=a
         self.b=b

      def value(self):
         x=df.fillna(self.b).groupby(self.a,dropna=False)['Sales2022'].sum()
         y=[]
         for i in x.index:
            m=x[i]*100/tsales22
            y.append([int(x[i]),i,round(m,2)])
         y=sorted(y, key=itemgetter(0), reverse=True)
         return y

   x3=sales22('Color','')
   ans=x3.value()
   arg['pst22']=ans

   x1=ans[0]
   arg['tecolor']=x1
   x1=ans[len(ans)-1]
   arg['tccolor']=x1

   x3=sales22('Power_Steering','NA')
   ans=x3.value()
   arg['pst22']=ans

   x3=sales22('Fuel_Type','')
   ans=x3.value()
   arg['ftype22']=ans

   x3=sales22('Body_Type','')
   ans=x3.value()
   arg['bdtype22']=ans

   x3=sales22('Front_Brakes','NA')
   ans=x3.value()
   arg['fbrtype22']=ans

   x3=sales22('Rear_Brakes','NA')
   ans=x3.value()
   arg['rbrtype22']=ans

   x1=df['Mileage'].max()
   arg['maxmile22']=x1
   x1=df['Mileage'].mode()
   arg['avgmile22']=x1
   x1=df['Mileage'].min()
   arg['minmile22']=x1


   x3=sales22('Emission_Norm','NA')
   ans=x3.value()
   arg['entype22']=ans

   x3=sales22('Front_Suspension','NA')
   ans=x3.value()
   x2=[ans[0],ans[1],ans[len(ans)-1]]
   arg['fs22']=x2

   x3=sales22('Rear_Suspension','NA')
   ans=x3.value()
   x2=[ans[0],ans[1],ans[len(ans)-1]]
   arg['rs22']=x2

   x3=sales22('Highest_sales_state','')
   ans=x3.value()
   x2=[ans[0],ans[1],ans[len(ans)-1]]
   arg['statesale22']=x2

   x3=sales22('Displacement','')
   ans=x3.value()
   arg['avgdisp22']=ans[0]
   

# ##############

   return render(req,'home.html',arg)


def explore(req):

   # FIGURES

   # SCATTER

   fig1 = px.scatter( df,y=df.Price, x=df.index,
                title="All Cars Prices",color=df.Cylinders,template="seaborn" ,render_mode="svg"
       ,hover_name='Tags',height=700,
       color_continuous_scale=px.colors.sequential.Plasma,
       hover_data={
         'Cylinders':False,
       })
   fig1.update_traces(marker_size=df.Sales2022/9000,showlegend=False,)
   fig1.update_xaxes(showgrid=False)
   fig1.update_yaxes(showgrid=False)
   fig1.update_layout(

    font_family="Verdana",
    font_color="white",
    title_font_size=24,
   #  title_font_color="white",
   #  legend_title_font_color="green",
    yaxis=dict(title='Price (INR)'),
    xaxis=dict(title='Model'),
    paper_bgcolor='#202020',
    plot_bgcolor='#202020',
)
   fig1.update_coloraxes(showscale=False)
   fig1 = plot(fig1, output_type='div', include_plotlyjs=False)
   arg={
      'f1':fig1
   }

# LINE

   cs2['Tags']=df['Tags'].copy()[pd.isna(df.Displacement)==False]
   # cs2["Displacement"] = cs2["Displacement"].str.rstrip(" cc")
   cs2['Cylinders']=df.Cylinders
   fig2 = px.line(cs2, x=cs2.index, y="Displacement", title='Cars : Enginne size vs Model',template='seaborn',hover_name='Tags',render_mode='svg')
   fig2.update_yaxes(showgrid=False,ticksuffix=' cc ',gridwidth=3)
   fig2.update_xaxes(showgrid=False)
   fig2.update_traces(showlegend=False,line=dict(
                           color='#fa6a28',
                           width=1
                     ),mode=' lines')
   fig2.update_coloraxes(showscale=False)
   fig2.update_layout(
      # hovermode="x",
   xaxis=dict(title='Model'),
   yaxis=dict(title='Engine size'),height=700,
   paper_bgcolor='#202020',
   plot_bgcolor='#202020',
   font_family="Verdana",
      font_color="white",
      title_font_size=24

      )
   fig2 = plot(fig2, output_type='div', include_plotlyjs=False)
   arg['f2']=fig2

# BAR


   fig3 = px.bar(brandsale22df,
                 y=brandsale22df.index,
                 x=brandsale22df.Sales2022,color=brandsale22df.Sales2022,
                 title='Cars : Brand vs Total Sales 2022',
               #   hover_name='Tags',
                 template='plotly_dark',
       color_continuous_scale=px.colors.sequential.Plasma,
                 )
   fig3.update_layout(
      title=dict({
      'x':0.5,
            'xanchor': 'center',
      }),
      hovermode="x unified",
   xaxis=dict(title='Total Sales in 2022'),
   yaxis=dict(title='Car brand'),height=840,
   paper_bgcolor='#202020',
   plot_bgcolor='#202020',
   font_family="Verdana",
    font_color="white",
    title_font_size=24

    )
   # fig1.update_xaxes()
   fig3.update_yaxes(showgrid=False,ticksuffix=' ')
   fig3.update_traces(width=1,showlegend=False,)
   fig3.update_coloraxes(showscale=False)

   fig3 = plot(fig3, output_type='div', include_plotlyjs=False)
   arg['f3']=fig3


# COLOR and SALES22

   color22df=df.groupby('Color')[['Sales2022','Sales2021']].sum()
   fig4 = px.pie(color22df, names=color22df.index,hole=.5,values=color22df.Sales2022,
             title='Popular Colors by Total Sales 2022',color=color22df.index,color_discrete_map={
       'white':'white',
       'red':'red',
       'maroon':'#911a24',
       'orange':'#e07516',
       'darkgreen':'green',
       'yellow':'yellow',
       'beige':'beige',
       'gray':'#78797a',
       'black':'#171717',
       'purple':'purple',
       'charcoal':'darkgray',
       'caramel':'brown',
       'blue':'#2259e3',
       'silver':'#b3b6bd',

    }
             )
   fig4.update_layout(
      title=dict({
      'x':0.5,
            'xanchor': 'center',
      }),
      hovermode="x unified",
   xaxis=dict(title='Total Sales in 2022'),
   yaxis=dict(title='Car brand'),height=600,
   paper_bgcolor='#202020',
   plot_bgcolor='#202020',
   font_family="Verdana",
    font_color="white",
    title_font_size=24

    )
   fig4.update_yaxes(showgrid=False,ticksuffix=' ')
   fig4.update_coloraxes(showscale=False)
   fig4.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
   fig4 = plot(fig4, output_type='div', include_plotlyjs=False)
   arg['f4']=fig4

# EMISSION NORM

   enorm22=df.groupby('Emission_Norm')[['Sales2022','Sales2021']].sum()
   fig5 = px.pie(enorm22, names=enorm22.index,hole=.5,values=enorm22.Sales2022,
             title='Emission Norms by Total Sales 2022',color=enorm22.index,color_discrete_map={
       'white':'white',
       'red':'red',
       'maroon':'#911a24',
       'orange':'#e07516',
       'darkgreen':'green',
       'yellow':'yellow',
       'beige':'beige',
       'gray':'#78797a',
       'black':'#171717',
       'purple':'purple',
       'charcoal':'darkgray',
       'caramel':'brown',
       'blue':'#2259e3',
       'silver':'#b3b6bd',

    }
             )
   fig5.update_layout(
      title=dict({
      'x':0.5,
            'xanchor': 'center',
      }),
      hovermode="x unified",
   xaxis=dict(title='Total Sales in 2022'),
   yaxis=dict(title='Car brand'),height=600,
   paper_bgcolor='#202020',
   plot_bgcolor='#202020',
   font_family="Verdana",
    font_color="white",
    title_font_size=24

    )
   fig5.update_yaxes(showgrid=False,ticksuffix=' ')
   fig5.update_coloraxes(showscale=False)
   fig5.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
   fig5 = plot(fig5, output_type='div', include_plotlyjs=False)
   arg['f5']=fig5

# STATE VS SALES22

   stsale22=df.groupby('Highest_sales_state')[['Sales2022','Sales2021']].sum()
   stsale22['State']=stsale22.index
   fig6 = px.histogram(stsale22, y='State', x=stsale22.Sales2022,
   color='State',
   template='plotly_dark',
   )
   fig6.update_yaxes(showgrid=False,ticksuffix=' ')
   fig6.update_xaxes(showgrid=False)
   fig6.update_traces(showlegend=False,
      # hovertemplate =
      # '<br><b>Total sales in 2022</b>: %{x}<br>'
      )

   fig6.update_coloraxes(showscale=False)
   fig6.update_layout(
      hovermode="y unified",
   xaxis=dict(title='Total sales in 2022'),
   yaxis=dict(title='States'),height=800,
   paper_bgcolor='#202020',
   plot_bgcolor='#202020',
   font_family="Verdana",
      font_color="white",
      title_font_size=24,
      )
   fig6 = plot(fig6, output_type='div', include_plotlyjs=False)
   arg['f6']=fig6


   return render(req,'db.html',arg)

def topsales(req):
   topsold22df=df.sort_values('Sales2022',ascending=False)[['Tags','Sales2022','Sales2021','Power','Emission_Norm','Body_Type','Fuel_Type','Gears','Mileage']]
   topsold22df.Mileage= topsold22df['Mileage'].fillna('--')
   topsold22df.Gears= topsold22df['Gears'].fillna('--')
   # topsold21df=topsold21df.round(2)
   topsold22df.rename(columns = {'Emission_Norm':'Emission norm','Tags':'Name','Body_Type':'Body type','Fuel_Type':'Fuel type'}, inplace = True)
   topsold22df=topsold22df[:20]


   topsold21df=df.sort_values('Sales2021',ascending=False)[['Tags','Sales2021','Sales2022','Power','Emission_Norm','Body_Type','Fuel_Type','Gears','Mileage']]
   topsold21df.Gears= topsold21df['Gears'].fillna('--')
   topsold21df.Mileage= topsold21df['Mileage'].fillna('--')
   topsold21df.rename(columns = {'Emission_Norm':'Emission norm','Tags':'Name','Body_Type':'Body type','Fuel_Type':'Fuel type'}, inplace = True)
   topsold21df=topsold21df[:20]

   topsold22html=topsold22df.to_html(classes='table table-borderless',justify='unset',index=False)
   topsold21html=topsold21df.to_html(classes='table table-borderless',justify='unset',index=False)
   arg={
   'topsales22':topsold22html,
   'topsales21':topsold21html,
   }

   return render(req,'topsales.html',arg)

