
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

class BookDataProcessor:
    def __init__(self, csv_path=None):
        """Initialize with optional CSV path for real dataset"""
        self.csv_path = csv_path
        self.df = None
        self.cleaned_df = None
        
    def load_sample_data(self):
        """Load sample tech books data"""
        data = {
            'book_id': range(1, 26),
            'title': [
                "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
                "Deep Learning", "Python Machine Learning", 
                "Reinforcement Learning: An Introduction",
                "Pattern Recognition and Machine Learning",
                "Deep Learning with Python", "The Hundred-Page Machine Learning Book",
                "Python for Data Analysis", "Introduction to Statistical Learning",
                "Natural Language Processing with Python",
                "Computer Vision: Algorithms and Applications",
                "Designing Machine Learning Systems", "Grokking Deep Learning",
                "Data Science from Scratch", "Algorithms",
                "Deep Reinforcement Learning Hands-On", "Fluent Python",
                "Speech and Language Processing", "Machine Learning Engineering",
                "Probabilistic Machine Learning: An Introduction",
                "Deep Learning for Computer Vision", "Python Data Science Handbook",
                "Introduction to Algorithms", "Effective Python",
                "Neural Networks and Deep Learning"
            ],
            'author': [
                "Aurélien Géron", "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                "Sebastian Raschka", "Richard S. Sutton, Andrew G. Barto",
                "Christopher M. Bishop", "François Chollet", "Andriy Burkov",
                "Wes McKinney", "Gareth James, Daniela Witten", "Steven Bird, Ewan Klein",
                "Richard Szeliski", "Chip Huyen", "Andrew Trask", "Joel Grus",
                "Robert Sedgewick, Kevin Wayne", "Maxim Lapan", "Luciano Ramalho",
                "Dan Jurafsky, James H. Martin", "Andriy Burkov", "Kevin Murphy",
                "Rajalingappaa Shanmugamani", "Jake VanderPlas", "Thomas H. Cormen",
                "Brett Slatkin", "Michael Nielsen"
            ],
            'category': [
                "Machine Learning", "Deep Learning", "Machine Learning", 
                "Reinforcement Learning", "Machine Learning", "Deep Learning",
                "Machine Learning", "Data Science", "Machine Learning", "NLP",
                "Computer Vision", "MLOps", "Deep Learning", "Data Science", "Algorithms",
                "Reinforcement Learning", "Python", "NLP", "MLOps", "Machine Learning",
                "Computer Vision", "Data Science", "Algorithms", "Python", "Deep Learning"
            ],
            'level': [
                "Intermediate", "Advanced", "Intermediate", "Advanced", "Advanced",
                "Beginner", "Beginner", "Beginner", "Intermediate", "Intermediate",
                "Advanced", "Intermediate", "Beginner", "Beginner", "Intermediate",
                "Intermediate", "Intermediate", "Advanced", "Intermediate", "Advanced",
                "Intermediate", "Intermediate", "Advanced", "Intermediate", "Beginner"
            ],
            'rating': [4.6, 4.5, 4.4, 4.7, 4.6, 4.5, 4.3, 4.4, 4.6, 4.2, 4.5, 4.7, 
                       4.4, 4.3, 4.5, 4.4, 4.7, 4.6, 4.5, 4.6, 4.3, 4.5, 4.5, 4.5, 4.7],
            'year': [2022, 2016, 2019, 2018, 2006, 2021, 2019, 2022, 2021, 2009, 
                     2022, 2022, 2019, 2019, 2011, 2020, 2022, 2023, 2020, 2022, 
                     2018, 2016, 2009, 2019, 2015],
            'num_reviews': [1250, 890, 750, 620, 450, 980, 340, 820, 710, 380,
                           560, 890, 420, 510, 890, 340, 920, 450, 380, 520,
                           290, 740, 1100, 560, 380]
        }
        self.df = pd.DataFrame(data)
        return self.df
    
    def load_from_csv(self):
        """Load data from CSV file"""
        if not self.csv_path:
            raise ValueError("CSV path not provided")
        
        self.df = pd.read_csv(self.csv_path)
        return self.df
    
    def clean_data(self):
        """Clean and preprocess the data"""
        self.cleaned_df = self.df.copy()
        
        # Handle missing values
        self.cleaned_df['title'] = self.cleaned_df['title'].fillna('Unknown')
        self.cleaned_df['author'] = self.cleaned_df['author'].fillna('Unknown')
        self.cleaned_df['rating'] = self.cleaned_df['rating'].fillna(self.cleaned_df['rating'].median())
        
        # Remove duplicates
        self.cleaned_df = self.cleaned_df.drop_duplicates(subset=['title', 'author'])
        
        # Clean text columns
        self.cleaned_df['title'] = self.cleaned_df['title'].str.strip()
        self.cleaned_df['author'] = self.cleaned_df['author'].str.strip()
        
        # Ensure rating is in valid range
        self.cleaned_df = self.cleaned_df[
            (self.cleaned_df['rating'] >= 0) & 
            (self.cleaned_df['rating'] <= 5)
        ]
        
        return self.cleaned_df
    
    def encode_features(self):
        """Encode categorical features"""
        le_category = LabelEncoder()
        le_level = LabelEncoder()
        
        self.cleaned_df['category_encoded'] = le_category.fit_transform(self.cleaned_df['category'])
        self.cleaned_df['level_encoded'] = le_level.fit_transform(self.cleaned_df['level'])
        
        return self.cleaned_df, le_category, le_level
    
    def get_statistics(self):
        """Get comprehensive statistics about the dataset"""
        stats = {
            'total_books': len(self.cleaned_df),
            'categories': self.cleaned_df['category'].value_counts().to_dict(),
            'levels': self.cleaned_df['level'].value_counts().to_dict(),
            'avg_rating': self.cleaned_df['rating'].mean(),
            'year_range': (self.cleaned_df['year'].min(), self.cleaned_df['year'].max()),
            'top_rated': self.cleaned_df.nlargest(5, 'rating')[['title', 'rating']].to_dict('records')
        }
        return stats
    
    def visualize_data(self, save_path='visualizations'):
        """Create visualizations of the dataset"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Category distribution
        self.cleaned_df['category'].value_counts().plot(kind='bar', ax=axes[0, 0], color='skyblue')
        axes[0, 0].set_title('Books by Category', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Category')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Level distribution
        self.cleaned_df['level'].value_counts().plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
        axes[0, 1].set_title('Books by Difficulty Level', fontsize=14, fontweight='bold')
        
        # 3. Rating distribution
        axes[1, 0].hist(self.cleaned_df['rating'], bins=20, color='lightcoral', edgecolor='black')
        axes[1, 0].set_title('Rating Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Rating')
        axes[1, 0].set_ylabel('Frequency')
        
        # 4. Books published over years
        year_counts = self.cleaned_df['year'].value_counts().sort_index()
        axes[1, 1].plot(year_counts.index, year_counts.values, marker='o', color='green')
        axes[1, 1].set_title('Books Published by Year', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Number of Books')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{save_path}/data_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {save_path}/data_analysis.png")
        
        return fig
    
    def export_cleaned_data(self, output_path='cleaned_books.csv'):
        """Export cleaned data to CSV"""
        if self.cleaned_df is None:
            raise ValueError("Data not cleaned yet. Run clean_data() first.")
        
        self.cleaned_df.to_csv(output_path, index=False)
        print(f"Cleaned data exported to {output_path}")
        return output_path
    
    def create_user_item_matrix(self, ratings_data):
        """Create user-item rating matrix for collaborative filtering"""
        # ratings_data should be a DataFrame with columns: user_id, book_id, rating
        matrix = ratings_data.pivot_table(
            index='user_id',
            columns='book_id',
            values='rating',
            fill_value=0
        )
        return matrix


# Example usage
if __name__ == "__main__":
    # Initialize processor
    processor = BookDataProcessor()
    
    # Load sample data
    print("Loading data...")
    df = processor.load_sample_data()
    print(f"Loaded {len(df)} books")
    
    # Clean data
    print("\nCleaning data...")
    cleaned_df = processor.clean_data()
    print(f"Cleaned data: {len(cleaned_df)} books")
    
    # Get statistics
    print("\nDataset Statistics:")
    stats = processor.get_statistics()
    print(f"Total Books: {stats['total_books']}")
    print(f"Average Rating: {stats['avg_rating']:.2f}")
    print(f"\nCategories:")
    for cat, count in stats['categories'].items():
        print(f"  {cat}: {count}")
    
    print(f"\nTop Rated Books:")
    for book in stats['top_rated']:
        print(f"  {book['title']}: {book['rating']}")
    
    # Encode features
    print("\nEncoding categorical features...")
    encoded_df, le_cat, le_level = processor.encode_features()
    
    # Export cleaned data
    print("\nExporting cleaned data...")
    processor.export_cleaned_data('tech_books_cleaned.csv')
    
    # Create visualizations
    print("\nCreating visualizations...")
    processor.visualize_data()

    print("\n✓ Data processing complete!")