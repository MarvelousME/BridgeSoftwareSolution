import React from 'react';

const Sidebar = () => {
    return (
        <aside className="sidebar">
            <h2>Sidebar Title</h2>
            <ul>
                <li><a href="/section1">Section 1</a></li>
                <li><a href="/section2">Section 2</a></li>
                <li><a href="/section3">Section 3</a></li>
                <li><a href="/section4">Section 4</a></li>
            </ul>
        </aside>
    );
};

export default Sidebar;

