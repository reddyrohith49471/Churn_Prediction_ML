from abc import ABC, abstractmethod

class BaseReport(ABC):

    @abstractmethod
    def run_and_save(self, reference_df, current_df, report_dir, timestamp):
        pass
    
    