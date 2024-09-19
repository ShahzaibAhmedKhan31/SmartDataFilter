export const setTableDataAction = (tableData) => {
    return (dispatch) => {
        dispatch({
            type: "SET_TABLE_DATA",
            payload: tableData
        });
    };
};

export const addFilterAction = (filter) => {
    return (dispatch) => {
        dispatch({
            type: "ADD_FILTER_ACTION",
            payload: filter
        });
    };
};

export const removeFilterAction = (filter) => {
    return (dispatch) => {
        dispatch({
            type: "REMOVE_FILTER_ACTION",
            payload: filter
        });
    };
};

export const clearFilterAction = () => {
    return (dispatch) => {
        dispatch({
            type: "Clear_FILTER_ACTION",
            payload: []
        });
    };
};