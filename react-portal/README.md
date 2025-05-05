# AI Portal - React Implementation

This folder contains a React implementation of the Enterprise AI Portal, providing a modern, responsive interface for accessing departmental AI applications.

## Advantages of React Over Dash

### Enhanced UI Flexibility
- **Component-Based Architecture:** Modular design for easier maintenance and reuse
- **Advanced Interactivity:** Smoother user interactions and animations
- **Customizable UI Patterns:** Greater flexibility in implementing complex UI components
- **Rich Ecosystem:** Access to thousands of pre-built components and libraries

### Better Performance
- **Virtual DOM:** Efficient rendering with React's virtual DOM
- **Code Splitting:** Faster initial load times by splitting code into smaller bundles
- **Client-Side Rendering:** Improved responsiveness with minimal server round-trips
- **React Router:** Seamless navigation without page reloads

### Developer Experience
- **Modern JavaScript:** Use the latest JavaScript features and patterns
- **Strong Community Support:** Large community with extensive resources and tutorials
- **Industry Standard:** Widely adopted in enterprise applications
- **Better Testing Tools:** Comprehensive testing frameworks

## Hybrid Implementation Strategy

This React implementation is designed to work alongside your existing Dash applications, allowing for a gradual migration:

1. **Phase 1: Side-by-side deployment**
   - Deploy React frontend with existing Dash applications
   - Connect React to Dash backends via API endpoints
   - Use React for UI-heavy pages, Dash for data visualization

2. **Phase 2: Enhanced integration**
   - Implement API gateway between React and Dash applications
   - Share authentication and session state between systems
   - Create unified navigation between React and Dash pages

3. **Phase 3: Optional full migration**
   - Migrate Dash features to React + Plotly.js as needed
   - Maintain Dash applications for complex visualizations if preferred
   - Achieve consistent UI experience across all components

## Connecting to Existing Dash Backends

The React implementation can connect to your existing Dash applications through API endpoints:

### Configuration

Edit the API integration in `src/api/config.js` to fetch data from your Dash backends:

```javascript
export const fetchConfig = async () => {
  const response = await axios.get('/api/config');
  return response.data;
};
```

### API Gateway Setup

1. Create API routes in your Dash application:

```python
@app.server.route('/api/config')
def serve_config():
    return jsonify(load_config())
```

2. Update the proxy setting in `package.json` to point to your Dash server:

```json
"proxy": "http://localhost:8050"
```

## Getting Started

1. Install dependencies:
```
npm install
```

2. Start development server:
```
npm start
```

3. Build for production:
```
npm run build
```

4. Serve production build (using simple Express server):
```
npx serve -s build
```

## Integration with Existing Assets

This React implementation is designed to leverage your existing assets:

- Uses the same images and icons from your `/assets` folder
- Maintains the same color scheme and design language
- Supports the same application configuration format

## Documentation

For detailed documentation on React components and integration patterns, see:

- [Components Documentation](./docs/components.md)
- [API Integration Guide](./docs/api-integration.md)
- [Migration Strategy](./docs/migration-strategy.md)