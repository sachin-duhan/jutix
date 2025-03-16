import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

class JMeterPlotter:
    def __init__(self, plots_dir: Path, logger: logging.Logger):
        self.plots_dir = plots_dir
        self.logger = logger
        
        # Set Seaborn style globally
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = [12, 6]
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['savefig.dpi'] = 100

    def get_plot_path(self, filename: str) -> str:
        """Get full path for plot files"""
        return str(self.plots_dir / filename)

    def plot_response_time_boxplot(self, df: pd.DataFrame, output_file='response_time_boxplot.png'):
        """Plot response time boxplot by file"""
        self.logger.info("Generating response time boxplot...")
        plt.figure(figsize=(15, 8))
        sns.boxplot(data=df, x='file', y='elapsed', palette='husl')
        plt.title('Response Time Distribution by Test File', pad=20)
        plt.xlabel('Test File')
        plt.ylabel('Response Time (ms)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        output_path = self.get_plot_path(output_file)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved boxplot to {output_path}")

    def plot_response_time_violin(self, df: pd.DataFrame, output_file='response_time_violin.png'):
        """Plot response time violin plot by file"""
        self.logger.info("Generating response time violin plot...")
        plt.figure(figsize=(15, 8))
        sns.violinplot(data=df, x='file', y='elapsed', palette='husl')
        plt.title('Response Time Density Distribution by Test File', pad=20)
        plt.xlabel('Test File')
        plt.ylabel('Response Time (ms)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        output_path = self.get_plot_path(output_file)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved violin plot to {output_path}")

    def plot_throughput_over_time(self, df: pd.DataFrame, output_file='throughput_over_time.png'):
        """Plot throughput over time"""
        self.logger.info("Generating throughput over time plot...")
        throughput = df.groupby(['file', 'second']).size().reset_index(name='count')
        plt.figure(figsize=(15, 8))
        sns.lineplot(data=throughput, x='second', y='count', hue='file', palette='husl')
        plt.title('Throughput Over Time', pad=20)
        plt.xlabel('Time')
        plt.ylabel('Requests per Second')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Test File', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        output_path = self.get_plot_path(output_file)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved throughput plot to {output_path}")

    def plot_response_time_percentiles(self, df: pd.DataFrame, output_file='response_time_percentiles.png'):
        """Plot response time percentiles by file"""
        self.logger.info("Generating response time percentiles plot...")
        percentiles = df.groupby('file')['elapsed'].describe(
            percentiles=[.50, .75, .90, .95, .99]
        ).round(2)
        
        plt.figure(figsize=(15, 8))
        ax = percentiles[['50%', '75%', '90%', '95%', '99%']].plot(kind='bar', width=0.8)
        plt.title('Response Time Percentiles by Test File', pad=20)
        plt.xlabel('Test File')
        plt.ylabel('Response Time (ms)')
        plt.legend(title='Percentile', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on the bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', padding=3, rotation=0)
            
        plt.tight_layout()
        output_path = self.get_plot_path(output_file)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved percentiles plot to {output_path}")

    def generate_all_plots(self, df: pd.DataFrame):
        """Generate all plots for the analysis"""
        self.plot_response_time_boxplot(df)
        self.plot_response_time_violin(df)
        self.plot_throughput_over_time(df)
        self.plot_response_time_percentiles(df) 