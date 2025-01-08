
import { BrowserRouter as Router, Routes, Route, createBrowserRouter, RouterProvider } from 'react-router-dom';
import { LandingAIPoc, Root1, Root2 } from '../pages';
import MainPage from '../pages/MainPage';
import MainFrame from '../Frame/MainFrame';
import ComponentDisplay from '../pages/ComponentDisplay';


const router = createBrowserRouter([
    {
        path : '/',
        element: <MainFrame/>,
        children: [
            {
                path: 'main',
                element: <MainPage />
            },
            {
                path: 'root1',
                element: <Root1 />
            },
            {
                path: 'root2',
                element: <Root2 />
            },
            {
                path: 'component_display',
                element: <ComponentDisplay />
            }
        ]

    }

]);


const AiPocRouter = () => {
    return <RouterProvider router={router}/>
    };

export default AiPocRouter;