from dataclasses import dataclass, field
from math import ceil
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class RoomDimensions:
    length1: float
    length2: float
    width1: float
    width2: float
    linter_spacing: float

@dataclass
class CeilingCalculation:
    parameters_full: int
    parameters_extra: float
    main_rods: int
    cross_rods: int
    connecting_clips: int
    screws: int
    total_parameter_length: float
    main_rods_length: float
    cross_rods_length: float
    l_patti_count: int
    black_screws: int
    fasteners: int
    fastener_clips: int
    board_count: float
    board_extra_sqft: float
    full_l_patti_count: int
    l_patti_cuts: int
    l_patti_remaining: int
    l_patti_cut_size: float
    last_cross_length: float
    cross_lengths: list[float] = field(default_factory=list)
    main_lengths: list[float] = field(default_factory=list)
    last_main_length: float = 0.0
    extra_main_needed: str = ""

def calculate_rod_length_with_overlap(length: float, standard_length: float = 12.0, overlap: float = 4/12) -> tuple[int, float]:
    if length <= standard_length:
        return 1, length
    
    full_rods = ceil((length - overlap) / (standard_length - overlap))
    total_length = length + ((full_rods - 1) * overlap)
    
    return full_rods, total_length

def calculate_parameters(dimensions: RoomDimensions) -> tuple[int, float]:
    STANDARD_LENGTH = 12
    OVERLAP = 4/12
    
    total_perimeter = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    
    full_rods = ceil(total_perimeter / STANDARD_LENGTH)
    
    extra_length = 0
    if total_perimeter > (full_rods * STANDARD_LENGTH):
        extra_length = total_perimeter - (full_rods * STANDARD_LENGTH)
        if extra_length > STANDARD_LENGTH:
            extra_length += OVERLAP
    
    return full_rods, round(extra_length, 2)

def calculate_main_rods(length1: float, length2: float, width1: float, width2: float) -> tuple[int, list[float], float, str]:
    FIRST_DISTANCE = 2
    SPACING = 4
    STANDARD_LENGTH = 12
    WALL_THRESHOLD = 3.5
    OVERLAP_INCHES = 5
    OVERLAP = OVERLAP_INCHES / 12
    
    positions = []
    current_pos = FIRST_DISTANCE
    
    while current_pos < width1:
        positions.append(current_pos)
        current_pos += SPACING

    remaining_space = width1 - positions[-1]
    if remaining_space >= WALL_THRESHOLD:
        positions.append(min(width1, positions[-1] + SPACING))
    
    main_lengths = []
    total_extra_needed = 0.0
    extra_rods_needed = 0
    
    for pos in positions:
        percentage = pos / width1
        length_at_pos = length1 + (length2 - length1) * (pos / width1)
        main_lengths.append(length_at_pos)
        
        if length_at_pos > STANDARD_LENGTH:
            extra_length = length_at_pos - STANDARD_LENGTH
            total_extra_needed += extra_length
            additional_rods_needed = ceil(extra_length / STANDARD_LENGTH)
            if additional_rods_needed > 0:
                total_extra_needed += (additional_rods_needed * OVERLAP)
            extra_rods_needed += additional_rods_needed
    
    main_count = len(positions) + extra_rods_needed
    extra_needed_str = f"{total_extra_needed:.2f} FT" if total_extra_needed > 0 else ""
    
    return main_count, main_lengths, main_lengths[-1] if main_lengths else 0, extra_needed_str

def calculate_cross_rods(length1: float, length2: float, width1: float, width2: float) -> tuple[int, list[float], float]:
    FIRST_DISTANCE = 2
    SPACING = 2
    MIN_THRESHOLD = 2
    MAX_THRESHOLD = 2.5
    OVERLAP = 4/12
    STANDARD_LENGTH = 12
    
    longer_wall = max(length1, length2)
    shorter_wall = min(length1, length2)
    
    positions = []
    current_pos = FIRST_DISTANCE
    
    while current_pos <= longer_wall:
        positions.append(current_pos)
        current_pos += SPACING
    
    if positions and (longer_wall - positions[-1]) <= MIN_THRESHOLD:
        positions.pop()
    
    if positions and (longer_wall - positions[-1]) > MAX_THRESHOLD:
        positions.append(positions[-1] + SPACING)
    
    cross_lengths = []
    for pos in positions:
        width_at_pos = width1 + (width2 - width1) * (pos / longer_wall)
        cross_lengths.append(width_at_pos)
    
    last_cross_length = cross_lengths[-1] if cross_lengths else 0
    
    total_cross_length = sum(cross_lengths)
    num_cross_rods = ceil(total_cross_length / STANDARD_LENGTH)
    
    return num_cross_rods, cross_lengths, last_cross_length

def calculate_l_patti(length: float, linter_spacing: float, main_lengths: list[float]) -> tuple[int, int, int, float]:
    L_PATTI_LENGTH = 8
    FIRST_L_PATTI = 3
    SPACING = 4
    
    def count_l_pattis_for_main(main_length: float) -> int:
        current_pos = FIRST_L_PATTI
        count = 0
        while current_pos <= (main_length - 1):
            count += 1
            current_pos += SPACING
        return count
    
    total_l_patti_cuts = 0
    for main_length in main_lengths:
        l_pattis_on_this_main = count_l_pattis_for_main(main_length)
        total_l_patti_cuts += l_pattis_on_this_main
    
    pieces_per_l_patti = int(L_PATTI_LENGTH / linter_spacing)
    full_l_patti_needed = ceil(total_l_patti_cuts / pieces_per_l_patti)
    
    total_pieces_available = full_l_patti_needed * pieces_per_l_patti
    remaining_pieces = total_pieces_available - total_l_patti_cuts
    
    return (full_l_patti_needed, total_l_patti_cuts, remaining_pieces, linter_spacing)

def calculate_board_requirements(dimensions: RoomDimensions) -> tuple[float, float]:
    BOARD_LENGTH = 6
    BOARD_WIDTH = 4
    BOARD_AREA = BOARD_LENGTH * BOARD_WIDTH
    
    room_area = ((dimensions.length1 + dimensions.length2) / 2) * ((dimensions.width1 + dimensions.width2) / 2)
    boards_needed = room_area / BOARD_AREA
    full_boards = int(boards_needed)
    extra_sqft = round((boards_needed - full_boards) * BOARD_AREA, 2)
    
    return full_boards, extra_sqft

def calculate_room_area(dimensions: RoomDimensions) -> float:
    avg_length = (dimensions.length1 + dimensions.length2) / 2
    avg_width = (dimensions.width1 + dimensions.width2) / 2
    return avg_length * avg_width

def calculate_ceiling_requirements(dimensions: RoomDimensions) -> CeilingCalculation:
    params_full, params_extra = calculate_parameters(dimensions)
    
    main_rods_count, main_lengths, last_main_length, extra_main_needed = calculate_main_rods(
        dimensions.length1,
        dimensions.length2,
        dimensions.width1,
        dimensions.width2
    )
    cross_rods_count, cross_lengths, last_cross_length = calculate_cross_rods(
        dimensions.length1,
        dimensions.length2,
        dimensions.width1,
        dimensions.width2
    )
    
    connecting_clips = main_rods_count * cross_rods_count
    
    total_parameter_length = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    
    screws = ceil(total_parameter_length) * 12
    
    full_l_patti, l_patti_cuts, remaining_cuts, cut_size = calculate_l_patti(
        max(dimensions.width1, dimensions.width2), 
        dimensions.linter_spacing,
        main_lengths
    )
    
    black_screws = l_patti_cuts * 2
    
    fasteners = l_patti_cuts
    fastener_clips = l_patti_cuts
    
    board_count, board_extra_sqft = calculate_board_requirements(dimensions)
    
    room_area = calculate_room_area(dimensions)
    black_screw_boxes = ceil(room_area / 1000)
    
    cross_rods_length = sum(cross_lengths)
    
    return CeilingCalculation(
        parameters_full=params_full,
        parameters_extra=round(params_extra, 2),
        main_rods=main_rods_count,
        cross_rods=cross_rods_count,
        connecting_clips=connecting_clips,
        screws=screws,
        total_parameter_length=round(total_parameter_length, 2),
        main_rods_length=round(sum(main_lengths), 2),
        cross_rods_length=round(cross_rods_length, 2),
        l_patti_count=l_patti_cuts,
        black_screws=black_screw_boxes,
        fasteners=fasteners,
        fastener_clips=fastener_clips,
        board_count=board_count,
        board_extra_sqft=board_extra_sqft,
        full_l_patti_count=full_l_patti,
        l_patti_cuts=l_patti_cuts,
        l_patti_remaining=remaining_cuts,
        l_patti_cut_size=cut_size,
        last_cross_length=round(last_cross_length, 2),
        cross_lengths=cross_lengths,
        main_lengths=main_lengths,
        last_main_length=round(last_main_length, 2),
        extra_main_needed=extra_main_needed
    )