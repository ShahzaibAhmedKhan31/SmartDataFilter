export const setTableDataReducer = (state = false, action) => {
    switch (action.type) {
        case "SET_TABLE_DATA":
            return action.payload;
        default:
            return state;
    }
};


export const filtersReducer = (state = [], action) => {
    switch (action.type) {
        case "ADD_FILTER_ACTION":
            return [...state, action.payload]; // Add new filter
        case "REMOVE_FILTER_ACTION":
            return state.filter(filter => filter !== action.payload); // Remove filter
        default:
            return state; // Return current state if no action matches
    }
};
