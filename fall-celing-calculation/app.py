import streamlit as st
import pandas as pd
from math import ceil
from decimal import Decimal
import base64
from io import BytesIO
from utils import RoomDimensions, calculate_ceiling_requirements
from translations import HINGLISH_TRANSLATIONS as TR

def convert_to_feet(value, unit):
    conversion = {
        'ft': 1.0,
        'mm': 0.00328084,
        'cm': 0.0328084,
        'inches': 0.0833333,
        'm': 3.28084,
        'yd': 3
    }
    return value * conversion[unit]

def generate_excel_download(calc_results):
    df = pd.DataFrame({
        'Item': [
            'Parameters (Full 12ft)',
            'Parameters (Extra Length)',
            'Main Rods',
            'Cross Rods',
            'Connecting Clips',
            'Screws',
            'Total Parameter Length'
        ],
        'Quantity': [
            calc_results.parameters_full,
            f"{calc_results.parameters_extra:.2f} ft",
            calc_results.main_rods,
            calc_results.cross_rods,
            calc_results.connecting_clips,
            calc_results.screws,
            f"{calc_results.total_parameter_length:.2f} ft"
        ]
    })
    
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Ceiling Calculation')
    
    return buffer.getvalue()

def convert_to_hinglish():
    st.title(TR['calculator_title'])
    unit = st.selectbox(TR['select_unit'], ['ft', 'mm', 'cm', 'inches', 'm', 'yd'])
    linter_spacing = st.number_input(f"{TR['linter_spacing']} ({unit})", min_value=0.0)
    st.subheader(TR['room_measurements'])
    col1, col2 = st.columns(2)
    
    with col1:
        length1 = st.number_input(f'{TR["wall1_length"]} ({unit})', min_value=0.0)
        width1 = st.number_input(f'{TR["wall1_width"]} ({unit})', min_value=0.0)
    
    with col2:
        length2 = st.number_input(f'{TR["wall2_length"]} ({unit})', min_value=0.0)
        width2 = st.number_input(f'{TR["wall2_width"]} ({unit})', min_value=0.0)

    if st.button(TR['calculate_button']):
        dimensions = RoomDimensions(
            convert_to_feet(length1, unit),
            convert_to_feet(length2, unit),
            convert_to_feet(width1, unit),
            convert_to_feet(width2, unit),
            convert_to_feet(linter_spacing, unit)
        )
        
        results = calculate_ceiling_requirements(dimensions)
        
        st.subheader(TR['calculation_results'])
        
        st.write(TR['parameters_title'])
        st.write(f"{TR['total_parameter_length']}: {results.total_parameter_length:.2f} ft")
        st.write(f"{TR['full_parameters']}: {results.parameters_full}")
        if results.parameters_extra > 0:
            st.write(f"{TR['extra_parameter_length']}: {results.parameters_extra:.2f} ft ({TR['overlap']})")
        
        st.write(TR['main_rods_title'])
        st.write(f"{TR['number_of_main_rods']}: {len(results.main_lengths)}")
        if results.extra_main_needed:
            extra_length = float(results.extra_main_needed.split()[0])
            extra_rods = ceil(extra_length / 12)
            st.write(f"{TR['extra_main_rods_needed']}: {extra_rods}")
            st.write(f"{TR['total_main_rods_needed']}: {len(results.main_lengths) + extra_rods}")
        st.write(TR['main_rods_details'])
        st.write(f"- {TR['first_rod']}: 2ft")
        st.write(f"- {TR['spacing_between_rods']}: 4ft")
        for i, length in enumerate(results.main_lengths):
            st.write(f"- {TR['main_rod']} {i+1}: {length:.2f} ft")
        st.write(f"- {TR['last_main_length']}: {results.last_main_length:.2f} ft")
        
        st.write(TR['cross_rods_title'])
        st.write(f"{TR['number_of_cross_rods']}: {results.cross_rods}")
        st.write(TR['cross_rods_details'])
        st.write(f"- {TR['first_rod']}: 2ft")
        st.write(f"- {TR['spacing_between_rods']}: 2ft")
        for i, length in enumerate(results.cross_lengths):
            st.write(f"- {TR['cross_rod']} {i+1}: {length:.2f} ft")
        st.write(f"- {TR['last_cross_length']}: {results.last_cross_length:.2f} ft")
        
        st.write(TR['support_materials_title'])
        st.write(f"{TR['full_l_patti_count']}: {results.full_l_patti_count}")
        st.write(f"{TR['cutting_l_patti']}: {results.l_patti_cuts} ({TR['cut_size']}: {results.l_patti_cut_size:.2f}ft/{TR['piece']})")
        st.write(f"{TR['remaining_cutted_l_patti']}: {results.l_patti_remaining} ({results.l_patti_cut_size:.2f}ft/{TR['piece']})")
        st.write(f"{TR['fasteners_needed']}: {results.fasteners} ({TR['per_l_patti']})")
        st.write(f"{TR['fastener_clips_needed']}: {results.fastener_clips} ({TR['per_fastener']})")
        st.write(f"{TR['nut_bolt_pair_needed']}: {results.fastener_clips} ({TR['per_fastener_clip']})")
        st.write(f"{TR['connecting_clips_needed']}: {results.connecting_clips} ({TR['at_main_cross_intersections']})")
        
        st.write(TR['screws_title'])
        st.write(f"{TR['regular_screws']}: {results.screws} ({TR['spacing_on_parameters']})")
        st.write(f"{TR['black_screws']}: {results.black_screws} {TR['box']} ({TR['per_1000_sqft']})")
        
        st.write(TR['plywood_boards_title'])
        if results.board_extra_sqft > 0:
            st.write(f"{TR['full_boards_needed']}: {int(results.board_count)}")
            st.write(f"{TR['extra_area_needed']}: {results.board_extra_sqft:.2f} sqft ({results.board_extra_sqft/24:.2f} {TR['boards']})")
        else:
            st.write(f"{TR['full_boards_needed']}: {int(results.board_count)}")

def main():
    st.set_page_config(page_title='Ceiling Design Calculator')
    st.title('Ceiling Design Calculator')
    
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    if st.session_state.language == 'English':
        if st.button('Convert to Hinglish'):
            st.session_state.language = 'Hinglish'
            st.rerun()
    else:
        if st.button('Convert to English'):
            st.session_state.language = 'English'
            st.rerun()
    
    if st.session_state.language == 'Hinglish':
        convert_to_hinglish()
    else:
        unit = st.selectbox(
            'Select measurement unit:',
            ['ft', 'mm', 'cm', 'inches', 'm', 'yd']
        )
        
        linter_spacing = st.number_input(
            f'Linter Spacing ({unit})',
            min_value=0.0,
            help="Distance from Roof/Linter to the Main/Enter"
        )
        
        st.subheader('Room Measurements')
        col1, col2 = st.columns(2)
        
        with col1:
            length1 = st.number_input(f'Wall 1 Length ({unit})', min_value=0.0)
            width1 = st.number_input(f'Wall 1 Width ({unit})', min_value=0.0)
        
        with col2:
            length2 = st.number_input(f'Wall 2 Length ({unit})', min_value=0.0)
            width2 = st.number_input(f'Wall 2 Width ({unit})', min_value=0.0)

        if st.button('Calculate'):
            dimensions = RoomDimensions(
                convert_to_feet(length1, unit),
                convert_to_feet(length2, unit),
                convert_to_feet(width1, unit),
                convert_to_feet(width2, unit),
                convert_to_feet(linter_spacing, unit)
            )
            
            results = calculate_ceiling_requirements(dimensions)
            
            st.subheader('Calculation Results')
            
            st.write("### Parameters (1 inch × 1 inch Steel Rods)")
            st.write(f"Total Perimeter Length: {results.total_parameter_length:.2f} ft")
            st.write(f"Full Parameters (12ft each): {results.parameters_full}")
            if results.parameters_extra > 0:
                st.write(f"Extra Parameter Length: {results.parameters_extra:.2f} ft (with 4 inch overlap)")
            
            st.write("### Main/Enter Rods (1 inch × 2 inch)")
            st.write(f"Number of Main Rods: {len(results.main_lengths)}")
            if results.extra_main_needed:
                extra_length = float(results.extra_main_needed.split()[0])
                extra_rods = ceil(extra_length / 12)
                st.write(f"Need Main Rod for Extra: {extra_rods}")
                st.write(f"Total Main Rod Needed: {len(results.main_lengths) + extra_rods}")
            st.write(f"Main Rod Details:")
            st.write("- First rod: 2ft from wall")
            st.write("- Spacing between rods: 4ft")
            for i, length in enumerate(results.main_lengths):
                st.write(f"- Main {i+1}: {length:.2f} ft")
            st.write(f"- Last Main Length: {results.last_main_length:.2f} ft")
            if results.extra_main_needed:
                st.write(f"Extra Main Needed: {results.extra_main_needed}")
            
            st.write("### Cross Rods (3 inch × 1 inch)")
            st.write(f"Number of Cross Rods: {results.cross_rods}")
            st.write("Cross Rod Details:")
            st.write("- First rod: 2ft from wall")
            st.write("- Spacing: 2ft between rods")
            for i, length in enumerate(results.cross_lengths):
                st.write(f"- Cross {i+1}: {length:.2f} ft")
            st.write(f"- Last Cross Length: {results.last_cross_length:.2f} ft")
            
            st.write("### Support Materials")
            st.write(f"Full L-Patti Count (8ft): {results.full_l_patti_count}")
            st.write(f"Cutting L-Patti: {results.l_patti_cuts} (Cut Size: {results.l_patti_cut_size:.2f}ft/piece)")
            st.write(f"Remaining Cutted L-Patti: {results.l_patti_remaining} ({results.l_patti_cut_size:.2f}ft/piece)")
            st.write(f"Fasteners needed: {results.fasteners} (1 per L-patti)")
            st.write(f"Fastener clips needed: {results.fastener_clips} (1 per fastener)")
            st.write(f"Nut Bolt Pair needed: {results.fastener_clips} (1 per Fastener Clip)")
            st.write(f"Connecting clips needed: {results.connecting_clips} (at Main-Cross intersections)")
            
            st.write("### Screws")
            st.write(f"Regular screws: {results.screws} (1ft spacing on parameters)")
            st.write(f"Black screws: {results.black_screws} Box(es) (1 Box per 1000 sqft)")
            
            st.write("### Plywood Boards (6ft × 4ft x 0.5inch)")
            if results.board_extra_sqft > 0:
                st.write(f"Full boards needed: {int(results.board_count)}")
                st.write(f"Extra area needed: {results.board_extra_sqft:.2f} sqft ({results.board_extra_sqft/24:.2f} boards)")
            else:
                st.write(f"Full boards needed: {int(results.board_count)}")

if __name__ == '__main__':
    main()