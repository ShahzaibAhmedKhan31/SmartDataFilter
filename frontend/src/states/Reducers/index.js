import { combineReducers } from 'redux';
import {setTableDataReducer} from './reducer';
import { filtersReducer } from './reducer';

const combinereducers = combineReducers({
    tableData: setTableDataReducer,
    filters: filtersReducer
})

export default combinereducers;
