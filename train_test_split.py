import pandas as pd
from sklearn.model_selection import train_test_split


data = pd.read_csv('/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset/annotations.csv')
print(data['label'].value_counts())

# First, split data into train+dev and test sets (e.g., 80% train+dev, 20% test)
train_dev_data, test_data = train_test_split(
    data, test_size=0.2, stratify=data['label'], random_state=42
)

# Now, split train+dev into train and dev sets (e.g., 75% train, 25% dev)
train_data, dev_data = train_test_split(
    train_dev_data, test_size=0.25, stratify=train_dev_data['label'], random_state=42
)

# Check class distribution in each set
print("Train set class distribution:\n", train_data['label'].value_counts())
print("Dev set class distribution:\n", dev_data['label'].value_counts())
print("Test set class distribution:\n", test_data['label'].value_counts())

train_data.to_csv('/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset/train.csv', index=False)
dev_data.to_csv('/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset/dev.csv', index=False)
test_data.to_csv('/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset/test.csv', index=False)