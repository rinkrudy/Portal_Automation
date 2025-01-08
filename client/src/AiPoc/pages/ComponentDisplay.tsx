import React, { FunctionComponent } from 'react';
import Layout from '../components/Layout';

import SideNavigation from '../components/SideNavigation';


export type ComponentDisplayType = {

}

const ComponentDisplay: FunctionComponent = () => {
    return (
      <div className='app-container'>
        <SideNavigation foldMode='partial' />
        <div className='content'>
          <Layout layout='three-column'>
            <div style={{ backgroundColor: 'lightcoral', padding: '16px' }}>Item 1</div>
            <div style={{ backgroundColor: 'lightblue', padding: '16px' }}>Item 2</div>
            <div style={{ backgroundColor: 'lightgreen', padding: '16px' }}>Item 3</div>
          </Layout>
        </div>
      </div>
    );
  };

export default ComponentDisplay;