import pandas as pd
import matplotlib.pyplot as plt


class RetailOrganizer:

    def __init__(self, file, product):
        self.file = file
        self.product = product
        self.product_data = pd.read_csv(fr"../retail/data/{self.file}")
        self.plot = plt


    def filter_data(self, data, limit):
        # removes products that are not related to what was searched
        self.product_data = self.clean(self.product_data)
        self.product_data = data[(data['title'].str.contains(self.product)) | (data['title'].str.contains('Apple'))]
        #self.product_datadata = self.product_datadata.sort_values(by=['price'], ascending=False).head(limit)
        return self.product_data


    def clean(self, data):
        # Converts numbered values to float types
        data['stars'] = data['stars'].astype(float)
        data['price'] = data['price'].str.replace('$', '')
        data['price'] = data['price'].str.replace(',', '')
        data['price'] = data['price'].astype(float)
        data['total_reviews'] = data['total_reviews'].str.replace('(', '')
        data['total_reviews'] = data['total_reviews'].str.replace(')', '')
        data['total_reviews'] = data['total_reviews'].str.replace(',', '')
        data['total_reviews'] = data['total_reviews'].astype(float)
        return data


    def get_sql_data(self):
        # returns the data in a format that can be used to create a sql database
        return self.product_data.to_sql('iphones', con='engine', if_exists='replace', index=False)


    def print_data(self, limit = 10):
        """limit: prints the top n products, defaults to 10"""
        print(self.filter_data(self.product_data, limit))
        print(self.product_data.shape)


    def get_data(self):
        return self.filter_data(self.product_data, 1000)
    

    def get_csv(self):
        self.product_data = self.filter_data(self.product_data, 1000)
        return self.product_data.to_csv(fr"../retail/data/{self.product}_data.csv", index=False)

        
    def plot_data(self):
        self.plot.subplot(3, 1, 1)
        self.plot.bar(self.product_data['title'], self.product_data['price'], color='limegreen', width=0.5)
        self.plot.xticks(rotation=-90, fontsize=0)
        self.plot.xlabel('Product')
        self.plot.ylabel('Price')
        self.plot.plot()

        ax = self.plot.gca()
        ax.set_facecolor('darkgreen')

        self.plot.subplot(3, 1, 2)
        self.plot.bar(self.product_data['title'], self.product_data['stars'], color='goldenrod', width=0.5)
        self.plot.xticks(rotation=-90, fontsize=0)
        self.plot.xlabel('Product')
        self.plot.ylabel('stars')
        self.plot.plot()

        ax = self.plot.gca()
        ax.set_facecolor('saddlebrown')

        self.plot.subplot(3, 1, 3)
        self.plot.bar(self.product_data['title'], self.product_data['total_reviews'], color='tomato', width=0.5)
        self.plot.xticks(rotation=-90, fontsize=4)
        self.plot.xlabel('Product')
        self.plot.ylabel('total_reviews')
        self.plot.plot()

        ax = self.plot.gca()
        ax.set_facecolor('maroon')

        self.plot.show()


if __name__ == "__main__":
    ro = RetailOrganizer('iphones.csv', 'iPhone')
    ro.get_csv()
