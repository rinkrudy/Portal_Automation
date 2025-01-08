
import React from 'react';
import Header from './header';
import { Outlet } from 'react-router-dom';


export default function MainFrame() {
    return (
        <div>
            <Header />
            <main>
                <Outlet></Outlet>
            </main>
        </div>
    );
}


