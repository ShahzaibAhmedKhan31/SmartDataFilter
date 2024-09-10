import { applyMiddleware, createStore, compose } from 'redux';
import combinereducers from './Reducers/index';
import { thunk } from 'redux-thunk';


const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const store = createStore(combinereducers, {}, composeEnhancers(applyMiddleware(thunk)));
