"""
EMI Calculator Module
Provides functions to calculate EMI, total payment, and affordability metrics
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EMI_DURATIONS, INTEREST_RATES


class EMICalculator:
    """
    Handles all EMI-related calculations
    """
    
    @staticmethod
    def calculate_emi(principal, annual_rate, duration_months):
        """
        Calculate monthly EMI using reducing balance method
        
        Formula: EMI = [P × r × (1+r)^n] / [(1+r)^n – 1]
        where:
            P = Principal loan amount
            r = Monthly interest rate (annual rate / 12)
            n = Number of monthly installments
        
        Args:
            principal (float): Product price or loan amount
            annual_rate (float): Annual interest rate (e.g., 0.12 for 12%)
            duration_months (int): EMI duration in months
        
        Returns:
            float: Monthly EMI amount
        """
        if principal <= 0:
            return 0
        
        if annual_rate == 0:
            # No interest case
            return principal / duration_months
        
        # Convert annual rate to monthly rate
        monthly_rate = annual_rate / 12
        
        # Calculate EMI using formula
        emi = (principal * monthly_rate * (1 + monthly_rate)**duration_months) / \
              ((1 + monthly_rate)**duration_months - 1)
        
        return round(emi, 2)
    
    @staticmethod
    def calculate_total_payment(emi, duration_months):
        """
        Calculate total payment over EMI period
        
        Args:
            emi (float): Monthly EMI amount
            duration_months (int): EMI duration in months
        
        Returns:
            float: Total amount paid
        """
        return round(emi * duration_months, 2)
    
    @staticmethod
    def calculate_total_interest(principal, emi, duration_months):
        """
        Calculate total interest paid
        
        Args:
            principal (float): Original principal amount
            emi (float): Monthly EMI amount
            duration_months (int): EMI duration in months
        
        Returns:
            float: Total interest paid
        """
        total_payment = EMICalculator.calculate_total_payment(emi, duration_months)
        total_interest = total_payment - principal
        return round(max(0, total_interest), 2)
    
    @staticmethod
    def calculate_max_affordable_price(max_emi, duration_months, annual_rate):
        """
        Calculate maximum affordable product price based on EMI limit
        
        Inverse of EMI formula to find principal:
        P = EMI × [(1+r)^n – 1] / [r × (1+r)^n]
        
        Args:
            max_emi (float): Maximum affordable monthly EMI
            duration_months (int): EMI duration in months
            annual_rate (float): Annual interest rate
        
        Returns:
            float: Maximum affordable product price
        """
        if max_emi <= 0:
            return 0
        
        if annual_rate == 0:
            # No interest case
            return max_emi * duration_months
        
        monthly_rate = annual_rate / 12
        
        # Inverse formula to calculate principal
        max_price = max_emi * ((1 + monthly_rate)**duration_months - 1) / \
                    (monthly_rate * (1 + monthly_rate)**duration_months)
        
        return round(max_price, 2)
    
    @staticmethod
    def calculate_affordability_score(required_emi, max_affordable_emi, credit_score=None, 
                                     existing_emi=0, monthly_income=0):
        """
        Calculate affordability score (0-1 scale, higher is better)
        
        Factors considered:
        1. EMI to max affordable EMI ratio (primary factor)
        2. Credit score (if available)
        3. Total EMI to income ratio
        
        Args:
            required_emi (float): EMI required for the product
            max_affordable_emi (float): Maximum EMI customer can afford
            credit_score (int, optional): Customer's credit score (300-850)
            existing_emi (float, optional): Existing EMI obligations
            monthly_income (float, optional): Monthly income
        
        Returns:
            float: Affordability score (0-1)
        """
        if max_affordable_emi <= 0:
            return 0.0
        
        # Primary factor: EMI affordability ratio
        emi_ratio = required_emi / max_affordable_emi
        
        if emi_ratio <= 0.5:
            base_score = 1.0
        elif emi_ratio <= 1.0:
            base_score = 1.5 - 0.5 * emi_ratio
        else:
            base_score = max(0, 1.0 / emi_ratio)
        
        # Credit score factor (if available)
        credit_factor = 1.0
        if credit_score is not None:
            if credit_score >= 750:
                credit_factor = 1.1
            elif credit_score >= 650:
                credit_factor = 1.0
            elif credit_score >= 550:
                credit_factor = 0.9
            else:
                credit_factor = 0.7
        
        # Total EMI burden factor (if income is available)
        burden_factor = 1.0
        if monthly_income > 0:
            total_emi = required_emi + existing_emi
            total_emi_ratio = total_emi / monthly_income
            
            if total_emi_ratio <= 0.4:
                burden_factor = 1.0
            elif total_emi_ratio <= 0.6:
                burden_factor = 0.9
            else:
                burden_factor = 0.7
        
        # Combine factors
        final_score = base_score * credit_factor * burden_factor
        
        # Normalize to 0-1 range
        final_score = min(1.0, max(0.0, final_score))
        
        return round(final_score, 4)
    
    @staticmethod
    def classify_risk(affordability_score):
        """
        Classify risk level based on affordability score
        
        Args:
            affordability_score (float): Affordability score (0-1)
        
        Returns:
            str: Risk level ('Low', 'Medium', or 'High')
        """
        from config import RISK_THRESHOLDS
        
        if affordability_score >= RISK_THRESHOLDS['low']:
            return 'Low'
        elif affordability_score >= RISK_THRESHOLDS['medium']:
            return 'Medium'
        else:
            return 'High'
    
    @staticmethod
    def get_emi_breakdown(principal, annual_rate, duration_months):
        """
        Get detailed EMI breakdown including principal and interest components
        
        Args:
            principal (float): Product price or loan amount
            annual_rate (float): Annual interest rate
            duration_months (int): EMI duration in months
        
        Returns:
            dict: EMI breakdown details
        """
        emi = EMICalculator.calculate_emi(principal, annual_rate, duration_months)
        total_payment = EMICalculator.calculate_total_payment(emi, duration_months)
        total_interest = EMICalculator.calculate_total_interest(principal, emi, duration_months)
        
        return {
            'principal': round(principal, 2),
            'monthly_emi': emi,
            'duration_months': duration_months,
            'annual_interest_rate': round(annual_rate * 100, 2),
            'total_payment': total_payment,
            'total_interest': total_interest,
            'interest_percentage': round((total_interest / principal) * 100, 2) if principal > 0 else 0
        }
    
    @staticmethod
    def compare_emi_options(principal, annual_rate, durations=None):
        """
        Compare EMI options for different durations
        
        Args:
            principal (float): Product price
            annual_rate (float): Annual interest rate
            durations (list, optional): List of durations to compare
        
        Returns:
            list: List of EMI breakdowns for each duration
        """
        if durations is None:
            durations = EMI_DURATIONS
        
        comparisons = []
        for duration in durations:
            breakdown = EMICalculator.get_emi_breakdown(principal, annual_rate, duration)
            comparisons.append(breakdown)
        
        return comparisons


def main():
    """
    Demo function to test EMI calculator
    """
    print("="*60)
    print("EMI Calculator Demo")
    print("="*60)
    
    # Example 1: Calculate EMI
    principal = 50000
    annual_rate = 0.12  # 12%
    duration = 12
    
    emi = EMICalculator.calculate_emi(principal, annual_rate, duration)
    print(f"\nExample 1: EMI Calculation")
    print(f"Product Price: ₹{principal:,.2f}")
    print(f"Interest Rate: {annual_rate*100}% per annum")
    print(f"Duration: {duration} months")
    print(f"Monthly EMI: ₹{emi:,.2f}")
    
    # Example 2: Calculate max affordable price
    max_emi = 5000
    print(f"\n\nExample 2: Max Affordable Price")
    print(f"Max Affordable EMI: ₹{max_emi:,.2f}")
    print(f"Duration: {duration} months")
    print(f"Interest Rate: {annual_rate*100}% per annum")
    
    max_price = EMICalculator.calculate_max_affordable_price(max_emi, duration, annual_rate)
    print(f"Max Affordable Product Price: ₹{max_price:,.2f}")
    
    # Example 3: Affordability score
    required_emi = 4500
    max_affordable = 6000
    credit_score = 720
    
    print(f"\n\nExample 3: Affordability Score")
    print(f"Required EMI: ₹{required_emi:,.2f}")
    print(f"Max Affordable EMI: ₹{max_affordable:,.2f}")
    print(f"Credit Score: {credit_score}")
    
    score = EMICalculator.calculate_affordability_score(required_emi, max_affordable, credit_score)
    risk = EMICalculator.classify_risk(score)
    print(f"Affordability Score: {score}")
    print(f"Risk Level: {risk}")
    
    # Example 4: EMI comparison
    print(f"\n\nExample 4: EMI Options Comparison")
    print(f"Product Price: ₹{principal:,.2f}")
    print(f"Interest Rate: {annual_rate*100}% per annum\n")
    
    comparisons = EMICalculator.compare_emi_options(principal, annual_rate, [6, 12, 18, 24])
    
    print(f"{'Duration':<10} {'Monthly EMI':<15} {'Total Payment':<15} {'Total Interest':<15}")
    print("-" * 60)
    for comp in comparisons:
        print(f"{comp['duration_months']:<10} ₹{comp['monthly_emi']:>12,.2f} "
              f"₹{comp['total_payment']:>13,.2f} ₹{comp['total_interest']:>13,.2f}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
