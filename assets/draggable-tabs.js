if(!window.draggableTabs) {
    window.draggableTabs = {};
}

window.draggableTabs = {
    initSortable: function(tabsElementId) {
        // Wait for document to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                initSortableLogic(tabsElementId);
            });
        } else {
            initSortableLogic(tabsElementId);
        }
        return true;
    }
};

function initSortableLogic(tabsElementId) {
    setTimeout(function() {
        const tabsEl = document.getElementById('draggable-tabs');
        
        if (!tabsEl || !window.Sortable) {
            console.error('Could not initialize draggable tabs. Missing element or Sortable library.');
            return;
        }
        
        // Initialize Sortable on the tabs element
        const sortable = Sortable.create(tabsEl, {
            animation: 150,
            ghostClass: 'tab-ghost',
            chosenClass: 'tab-chosen',
            dragClass: 'tab-drag',
            handle: '.draggable-tab',
            // Save order to localStorage when finished dragging
            onEnd: function(evt) {
                const tabOrder = Array.from(tabsEl.children).map(el => el.dataset.tabId);
                localStorage.setItem('tabOrder', JSON.stringify(tabOrder));
                console.log('Tab order saved:', tabOrder);
            }
        });
        
        // Load order from localStorage if exists
        const savedOrder = localStorage.getItem('tabOrder');
        if (savedOrder) {
            try {
                const orderArray = JSON.parse(savedOrder);
                
                // Sort DOM elements based on saved order
                for (let i = 0; i < orderArray.length; i++) {
                    const tabId = orderArray[i];
                    const tabEl = Array.from(tabsEl.children).find(el => el.dataset.tabId === tabId);
                    if (tabEl) {
                        tabsEl.appendChild(tabEl); // Move to the end in the correct order
                    }
                }
            } catch (e) {
                console.error('Error restoring tab order:', e);
            }
        }
    }, 500); // Short delay to ensure DOM is fully loaded
}