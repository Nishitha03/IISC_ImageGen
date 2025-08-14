// import React, { useState, useEffect } from 'react';

// const StoryGeneratorApp = () => {
//   // State management
//   const [currentStory, setCurrentStory] = useState(null);
//   const [isGenerating, setIsGenerating] = useState(false);
//   const [isRefining, setIsRefining] = useState({ character: false, background: false, smart: false });
//   const [userPrompt, setUserPrompt] = useState('');
//   const [refinementPrompts, setRefinementPrompts] = useState({
//     character: '',
//     background: '',
//     characterAdjustments: '',
//     backgroundAdjustments: ''
//   });
//   const [activeTab, setActiveTab] = useState('generate');
//   const [error, setError] = useState('');

//   // API Base URL
//   const API_BASE = 'http://localhost:8000/api';

//   // Generate initial story
//   const generateStory = async () => {
//     if (!userPrompt.trim()) {
//       setError('Please enter a story prompt');
//       return;
//     }

//     setIsGenerating(true);
//     setError('');

//     try {
//       const response = await fetch(`${API_BASE}/generate/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ prompt: userPrompt }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();
//       setCurrentStory(data);
//       setActiveTab('refine');
//     } catch (error) {
//       setError(`Error generating story: ${error.message}`);
//     } finally {
//       setIsGenerating(false);
//     }
//   };

//   // Refine character image
//   const refineCharacter = async () => {
//     if (!currentStory || !refinementPrompts.character.trim()) {
//       setError('Please enter a character refinement prompt');
//       return;
//     }

//     setIsRefining(prev => ({ ...prev, character: true }));
//     setError('');

//     try {
//       const response = await fetch(`${API_BASE}/refine/character/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           story_id: currentStory.id,
//           refinement_prompt: refinementPrompts.character,
//           strength: 0.4
//         }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();
//       setCurrentStory(data);
//       setRefinementPrompts(prev => ({ ...prev, character: '' }));
//     } catch (error) {
//       setError(`Error refining character: ${error.message}`);
//     } finally {
//       setIsRefining(prev => ({ ...prev, character: false }));
//     }
//   };

//   // Refine background image
//   const refineBackground = async () => {
//     if (!currentStory || !refinementPrompts.background.trim()) {
//       setError('Please enter a background refinement prompt');
//       return;
//     }

//     setIsRefining(prev => ({ ...prev, background: true }));
//     setError('');

//     try {
//       const response = await fetch(`${API_BASE}/refine/background/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           story_id: currentStory.id,
//           refinement_prompt: refinementPrompts.background,
//           strength: 0.4
//         }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();
//       setCurrentStory(data);
//       setRefinementPrompts(prev => ({ ...prev, background: '' }));
//     } catch (error) {
//       setError(`Error refining background: ${error.message}`);
//     } finally {
//       setIsRefining(prev => ({ ...prev, background: false }));
//     }
//   };

//   // Smart scene refinement
//   const smartRefine = async () => {
//     if (!currentStory) return;
    
//     if (!refinementPrompts.characterAdjustments.trim() && !refinementPrompts.backgroundAdjustments.trim()) {
//       setError('Please enter at least one adjustment for smart refinement');
//       return;
//     }

//     setIsRefining(prev => ({ ...prev, smart: true }));
//     setError('');

//     try {
//       const response = await fetch(`${API_BASE}/refine/smart/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           story_id: currentStory.id,
//           character_adjustments: refinementPrompts.characterAdjustments,
//           background_adjustments: refinementPrompts.backgroundAdjustments
//         }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();
//       setCurrentStory(data);
//       setRefinementPrompts(prev => ({ 
//         ...prev, 
//         characterAdjustments: '', 
//         backgroundAdjustments: '' 
//       }));
//     } catch (error) {
//       setError(`Error in smart refinement: ${error.message}`);
//     } finally {
//       setIsRefining(prev => ({ ...prev, smart: false }));
//     }
//   };

//   return (
//     <div style={styles.container}>
//       {/* Header */}
//       <header style={styles.header}>
//         <h1 style={styles.title}>🎨 Interactive Story Generator</h1>
//         <p style={styles.subtitle}>Create stories with AI-generated images and refine them continuously</p>
//       </header>

//       {/* Error Display */}
//       {error && (
//         <div style={styles.error}>
//           <span>⚠️ {error}</span>
//           <button style={styles.errorClose} onClick={() => setError('')}>×</button>
//         </div>
//       )}

//       {/* Tab Navigation */}
//       <nav style={styles.nav}>
//         <button 
//           style={{...styles.tab, ...(activeTab === 'generate' ? styles.activeTab : {})}}
//           onClick={() => setActiveTab('generate')}
//         >
//           🚀 Generate Story
//         </button>
//         <button 
//           style={{...styles.tab, ...(activeTab === 'refine' ? styles.activeTab : {})}}
//           onClick={() => setActiveTab('refine')}
//           disabled={!currentStory}
//         >
//           🎯 Refine Images
//         </button>
//         <button 
//           style={{...styles.tab, ...(activeTab === 'view' ? styles.activeTab : {})}}
//           onClick={() => setActiveTab('view')}
//           disabled={!currentStory}
//         >
//           👁️ View Story
//         </button>
//       </nav>

//       {/* Generate Tab */}
//       {activeTab === 'generate' && (
//         <div style={styles.section}>
//           <h2 style={styles.sectionTitle}>Generate New Story</h2>
//           <div style={styles.inputGroup}>
//             <label style={styles.label}>Story Prompt:</label>
//             <textarea
//               style={styles.textarea}
//               value={userPrompt}
//               onChange={(e) => setUserPrompt(e.target.value)}
//               placeholder="Enter your story idea... (e.g., 'A brave knight discovers a magical library')"
//               rows={3}
//             />
//           </div>
//           <button 
//             style={{...styles.button, ...styles.primaryButton}}
//             onClick={generateStory}
//             disabled={isGenerating}
//           >
//             {isGenerating ? '🔄 Generating...' : '✨ Generate Story'}
//           </button>
//         </div>
//       )}

//       {/* Refine Tab */}
//       {activeTab === 'refine' && currentStory && (
//         <div style={styles.section}>
//           <h2 style={styles.sectionTitle}>Refine Your Images</h2>
          
//           {/* Current Images Display */}
//           <div style={styles.imageGrid}>
//             <div style={styles.imageContainer}>
//               <h3 style={styles.imageTitle}>Character</h3>
//               {currentStory.character_image_url && (
//                 <img 
//                   src={`http://localhost:8000${currentStory.character_image_url}`}
//                   alt="Character"
//                   style={styles.image}
//                 />
//               )}
//             </div>
//             <div style={styles.imageContainer}>
//               <h3 style={styles.imageTitle}>Background</h3>
//               {currentStory.background_image_url && (
//                 <img 
//                   src={`http://localhost:8000${currentStory.background_image_url}`}
//                   alt="Background"
//                   style={styles.image}
//                 />
//               )}
//             </div>
//             <div style={styles.imageContainer}>
//               <h3 style={styles.imageTitle}>Combined</h3>
//               {currentStory.combined_image_url && (
//                 <img 
//                   src={`http://localhost:8000${currentStory.combined_image_url}`}
//                   alt="Combined"
//                   style={styles.image}
//                 />
//               )}
//             </div>
//           </div>

//           {/* Individual Refinement Controls */}
//           <div style={styles.refinementGrid}>
//             {/* Character Refinement */}
//             <div style={styles.refinementCard}>
//               <h3 style={styles.cardTitle}>🎭 Refine Character</h3>
//               <textarea
//                 style={styles.refinementInput}
//                 value={refinementPrompts.character}
//                 onChange={(e) => setRefinementPrompts(prev => ({
//                   ...prev, character: e.target.value
//                 }))}
//                 placeholder="e.g., 'knight, heroic stance, confident expression, dramatic lighting'"
//                 rows={2}
//               />
//               <button 
//                 style={{...styles.button, ...styles.secondaryButton}}
//                 onClick={refineCharacter}
//                 disabled={isRefining.character}
//               >
//                 {isRefining.character ? '🔄 Refining...' : '🎨 Refine Character'}
//               </button>
//             </div>

//             {/* Background Refinement */}
//             <div style={styles.refinementCard}>
//               <h3 style={styles.cardTitle}>🏞️ Refine Background</h3>
//               <textarea
//                 style={styles.refinementInput}
//                 value={refinementPrompts.background}
//                 onChange={(e) => setRefinementPrompts(prev => ({
//                   ...prev, background: e.target.value
//                 }))}
//                 placeholder="e.g., 'castle courtyard, empty center space, organized layout'"
//                 rows={2}
//               />
//               <button 
//                 style={{...styles.button, ...styles.secondaryButton}}
//                 onClick={refineBackground}
//                 disabled={isRefining.background}
//               >
//                 {isRefining.background ? '🔄 Refining...' : '🎨 Refine Background'}
//               </button>
//             </div>
//           </div>

//           {/* Smart Refinement */}
//           <div style={styles.smartRefinement}>
//             <h3 style={styles.cardTitle}>🧠 Smart Scene Refinement</h3>
//             <div style={styles.smartInputs}>
//               <div style={styles.inputGroup}>
//                 <label style={styles.label}>Character Adjustments:</label>
//                 <input
//                   style={styles.input}
//                   value={refinementPrompts.characterAdjustments}
//                   onChange={(e) => setRefinementPrompts(prev => ({
//                     ...prev, characterAdjustments: e.target.value
//                   }))}
//                   placeholder="e.g., 'knight, library lighting, scholarly pose'"
//                 />
//               </div>
//               <div style={styles.inputGroup}>
//                 <label style={styles.label}>Background Adjustments:</label>
//                 <input
//                   style={styles.input}
//                   value={refinementPrompts.backgroundAdjustments}
//                   onChange={(e) => setRefinementPrompts(prev => ({
//                     ...prev, backgroundAdjustments: e.target.value
//                   }))}
//                   placeholder="e.g., 'library, knight-scale furniture, reading space'"
//                 />
//               </div>
//             </div>
//             <button 
//               style={{...styles.button, ...styles.accentButton}}
//               onClick={smartRefine}
//               disabled={isRefining.smart}
//             >
//               {isRefining.smart ? '🔄 Smart Refining...' : '✨ Smart Refine Both'}
//             </button>
//           </div>
//         </div>
//       )}

//       {/* View Tab */}
//       {activeTab === 'view' && currentStory && (
//         <div style={styles.section}>
//           <h2 style={styles.sectionTitle}>Your Story</h2>
          
//           {/* Story Text */}
//           <div style={styles.storyContainer}>
//             <h3 style={styles.storyTitle}>📖 Story</h3>
//             <p style={styles.storyText}>{currentStory.short_story}</p>
//           </div>

//           {/* Character Description */}
//           <div style={styles.descriptionContainer}>
//             <h3 style={styles.descriptionTitle}>🎭 Character Description</h3>
//             <p style={styles.descriptionText}>{currentStory.character_description}</p>
//           </div>

//           {/* Background Description */}
//           <div style={styles.descriptionContainer}>
//             <h3 style={styles.descriptionTitle}>🏞️ Background Description</h3>
//             <p style={styles.descriptionText}>{currentStory.background_description}</p>
//           </div>

//           {/* Final Combined Image */}
//           <div style={styles.finalImageContainer}>
//             <h3 style={styles.imageTitle}>🎨 Final Scene</h3>
//             {currentStory.combined_image_url && (
//               <img 
//                 src={`http://localhost:8000${currentStory.combined_image_url}`}
//                 alt="Final Combined Scene"
//                 style={styles.finalImage}
//               />
//             )}
//           </div>
//         </div>
//       )}

//       {/* Footer */}
//       <footer style={styles.footer}>
//         <p>Made with ❤️ using Django + LangChain + Stable Diffusion</p>
//       </footer>
//     </div>
//   );
// };

// // Styles object
// const styles = {
//   container: {
//     fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
//     maxWidth: '1200px',
//     margin: '0 auto',
//     padding: '20px',
//     backgroundColor: '#f8f9fa',
//     minHeight: '100vh',
//   },
//   header: {
//     textAlign: 'center',
//     marginBottom: '30px',
//     padding: '20px',
//     backgroundColor: '#ffffff',
//     borderRadius: '12px',
//     boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
//   },
//   title: {
//     color: '#2c3e50',
//     fontSize: '2.5rem',
//     margin: '0 0 10px 0',
//     fontWeight: '700',
//   },
//   subtitle: {
//     color: '#6c757d',
//     fontSize: '1.1rem',
//     margin: 0,
//   },
//   error: {
//     backgroundColor: '#f8d7da',
//     color: '#721c24',
//     padding: '12px 16px',
//     borderRadius: '8px',
//     marginBottom: '20px',
//     border: '1px solid #f5c6cb',
//     display: 'flex',
//     justifyContent: 'space-between',
//     alignItems: 'center',
//   },
//   errorClose: {
//     background: 'none',
//     border: 'none',
//     fontSize: '20px',
//     cursor: 'pointer',
//     color: '#721c24',
//   },
//   nav: {
//     display: 'flex',
//     gap: '10px',
//     marginBottom: '30px',
//     backgroundColor: '#ffffff',
//     padding: '10px',
//     borderRadius: '12px',
//     boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
//   },
//   tab: {
//     flex: 1,
//     padding: '12px 24px',
//     border: 'none',
//     borderRadius: '8px',
//     cursor: 'pointer',
//     fontSize: '1rem',
//     fontWeight: '600',
//     transition: 'all 0.3s ease',
//     backgroundColor: '#e9ecef',
//     color: '#495057',
//   },
//   activeTab: {
//     backgroundColor: '#007bff',
//     color: '#ffffff',
//     transform: 'translateY(-2px)',
//     boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
//   },
//   section: {
//     backgroundColor: '#ffffff',
//     padding: '30px',
//     borderRadius: '12px',
//     boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
//     marginBottom: '20px',
//   },
//   sectionTitle: {
//     color: '#2c3e50',
//     fontSize: '1.8rem',
//     marginBottom: '25px',
//     fontWeight: '700',
//   },
//   inputGroup: {
//     marginBottom: '20px',
//   },
//   label: {
//     display: 'block',
//     marginBottom: '8px',
//     color: '#495057',
//     fontWeight: '600',
//   },
//   input: {
//     width: '100%',
//     padding: '12px 16px',
//     border: '2px solid #e9ecef',
//     borderRadius: '8px',
//     fontSize: '1rem',
//     transition: 'border-color 0.3s ease',
//     boxSizing: 'border-box',
//   },
//   textarea: {
//     width: '100%',
//     padding: '12px 16px',
//     border: '2px solid #e9ecef',
//     borderRadius: '8px',
//     fontSize: '1rem',
//     transition: 'border-color 0.3s ease',
//     resize: 'vertical',
//     boxSizing: 'border-box',
//   },
//   button: {
//     padding: '12px 24px',
//     border: 'none',
//     borderRadius: '8px',
//     cursor: 'pointer',
//     fontSize: '1rem',
//     fontWeight: '600',
//     transition: 'all 0.3s ease',
//     textAlign: 'center',
//   },
//   primaryButton: {
//     backgroundColor: '#007bff',
//     color: '#ffffff',
//     boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
//   },
//   secondaryButton: {
//     backgroundColor: '#28a745',
//     color: '#ffffff',
//     boxShadow: '0 4px 12px rgba(40,167,69,0.3)',
//   },
//   accentButton: {
//     backgroundColor: '#dc3545',
//     color: '#ffffff',
//     boxShadow: '0 4px 12px rgba(220,53,69,0.3)',
//   },
//   imageGrid: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
//     gap: '20px',
//     marginBottom: '30px',
//   },
//   imageContainer: {
//     textAlign: 'center',
//   },
//   imageTitle: {
//     color: '#495057',
//     fontSize: '1.2rem',
//     marginBottom: '10px',
//     fontWeight: '600',
//   },
//   image: {
//     width: '100%',
//     maxWidth: '200px',
//     height: 'auto',
//     borderRadius: '8px',
//     boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
//     transition: 'transform 0.3s ease',
//   },
//   refinementGrid: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
//     gap: '20px',
//     marginBottom: '30px',
//   },
//   refinementCard: {
//     padding: '20px',
//     backgroundColor: '#f8f9fa',
//     borderRadius: '10px',
//     border: '2px solid #e9ecef',
//   },
//   cardTitle: {
//     color: '#495057',
//     fontSize: '1.3rem',
//     marginBottom: '15px',
//     fontWeight: '600',
//   },
//   refinementInput: {
//     width: '100%',
//     padding: '10px 14px',
//     border: '2px solid #dee2e6',
//     borderRadius: '6px',
//     fontSize: '0.95rem',
//     marginBottom: '15px',
//     resize: 'vertical',
//     boxSizing: 'border-box',
//   },
//   smartRefinement: {
//     padding: '25px',
//     backgroundColor: '#f1f3f4',
//     borderRadius: '12px',
//     border: '2px solid #dee2e6',
//   },
//   smartInputs: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
//     gap: '20px',
//     marginBottom: '20px',
//   },
//   storyContainer: {
//     backgroundColor: '#f8f9fa',
//     padding: '20px',
//     borderRadius: '10px',
//     marginBottom: '20px',
//   },
//   storyTitle: {
//     color: '#495057',
//     fontSize: '1.4rem',
//     marginBottom: '15px',
//     fontWeight: '600',
//   },
//   storyText: {
//     color: '#212529',
//     fontSize: '1.1rem',
//     lineHeight: '1.6',
//     margin: 0,
//   },
//   descriptionContainer: {
//     backgroundColor: '#f8f9fa',
//     padding: '15px',
//     borderRadius: '8px',
//     marginBottom: '15px',
//   },
//   descriptionTitle: {
//     color: '#495057',
//     fontSize: '1.2rem',
//     marginBottom: '10px',
//     fontWeight: '600',
//   },
//   descriptionText: {
//     color: '#495057',
//     fontSize: '1rem',
//     lineHeight: '1.5',
//     margin: 0,
//   },
//   finalImageContainer: {
//     textAlign: 'center',
//     marginTop: '30px',
//   },
//   finalImage: {
//     maxWidth: '100%',
//     height: 'auto',
//     borderRadius: '12px',
//     boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
//   },
//   footer: {
//     textAlign: 'center',
//     marginTop: '40px',
//     padding: '20px',
//     color: '#6c757d',
//     fontSize: '0.9rem',
//   },
// };

// export default StoryGeneratorApp;

import React, { useState, useEffect } from 'react';

const StoryGeneratorApp = () => {
  // State management
  const [currentStory, setCurrentStory] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRefining, setIsRefining] = useState({ character: false, background: false, smart: false });
  const [userPrompt, setUserPrompt] = useState('');
  const [refinementPrompts, setRefinementPrompts] = useState({
    character: '',
    background: '',
    characterAdjustments: '',
    backgroundAdjustments: ''
  });
  const [strengthValues, setStrengthValues] = useState({
    character: 0.4,
    background: 0.4,
    smart: 0.4
  });
  const [activeTab, setActiveTab] = useState('generate');
  const [error, setError] = useState('');

  // API Base URL
  const API_BASE = 'http://localhost:8000/api';

  // Generate initial story
  const generateStory = async () => {
    if (!userPrompt.trim()) {
      setError('Please enter a story prompt');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: userPrompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCurrentStory(data);
      setActiveTab('refine');
    } catch (error) {
      setError(`Error generating story: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  // Refine character image
  const refineCharacter = async () => {
    if (!currentStory || !refinementPrompts.character.trim()) {
      setError('Please enter a character refinement prompt');
      return;
    }

    setIsRefining(prev => ({ ...prev, character: true }));
    setError('');

    try {
      const response = await fetch(`${API_BASE}/refine/character/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story_id: currentStory.id,
          refinement_prompt: refinementPrompts.character,
          strength: strengthValues.character
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCurrentStory(data);
      setRefinementPrompts(prev => ({ ...prev, character: '' }));
    } catch (error) {
      setError(`Error refining character: ${error.message}`);
    } finally {
      setIsRefining(prev => ({ ...prev, character: false }));
    }
  };

  // Refine background image
  const refineBackground = async () => {
    if (!currentStory || !refinementPrompts.background.trim()) {
      setError('Please enter a background refinement prompt');
      return;
    }

    setIsRefining(prev => ({ ...prev, background: true }));
    setError('');

    try {
      const response = await fetch(`${API_BASE}/refine/background/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story_id: currentStory.id,
          refinement_prompt: refinementPrompts.background,
          strength: strengthValues.background
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCurrentStory(data);
      setRefinementPrompts(prev => ({ ...prev, background: '' }));
    } catch (error) {
      setError(`Error refining background: ${error.message}`);
    } finally {
      setIsRefining(prev => ({ ...prev, background: false }));
    }
  };

  // Smart scene refinement
  const smartRefine = async () => {
    if (!currentStory) return;
    
    if (!refinementPrompts.characterAdjustments.trim() && !refinementPrompts.backgroundAdjustments.trim()) {
      setError('Please enter at least one adjustment for smart refinement');
      return;
    }

    setIsRefining(prev => ({ ...prev, smart: true }));
    setError('');

    try {
      const response = await fetch(`${API_BASE}/refine/smart/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story_id: currentStory.id,
          character_adjustments: refinementPrompts.characterAdjustments,
          background_adjustments: refinementPrompts.backgroundAdjustments,
          strength: strengthValues.smart
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCurrentStory(data);
      setRefinementPrompts(prev => ({ 
        ...prev, 
        characterAdjustments: '', 
        backgroundAdjustments: '' 
      }));
    } catch (error) {
      setError(`Error in smart refinement: ${error.message}`);
    } finally {
      setIsRefining(prev => ({ ...prev, smart: false }));
    }
  };

  // Handle strength value changes
  const handleStrengthChange = (type, value) => {
    const numValue = parseFloat(value);
    if (numValue >= 0 && numValue <= 1) {
      setStrengthValues(prev => ({ ...prev, [type]: numValue }));
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>🎨 Interactive Story Generator</h1>
        <p style={styles.subtitle}>Create stories with AI-generated images and refine them continuously</p>
      </header>

      {/* Error Display */}
      {error && (
        <div style={styles.error}>
          <span>⚠️ {error}</span>
          <button style={styles.errorClose} onClick={() => setError('')}>×</button>
        </div>
      )}

      {/* Tab Navigation */}
      <nav style={styles.nav}>
        <button 
          style={{...styles.tab, ...(activeTab === 'generate' ? styles.activeTab : {})}}
          onClick={() => setActiveTab('generate')}
        >
          🚀 Generate Story
        </button>
        <button 
          style={{...styles.tab, ...(activeTab === 'refine' ? styles.activeTab : {})}}
          onClick={() => setActiveTab('refine')}
          disabled={!currentStory}
        >
          🎯 Refine Images
        </button>
        <button 
          style={{...styles.tab, ...(activeTab === 'view' ? styles.activeTab : {})}}
          onClick={() => setActiveTab('view')}
          disabled={!currentStory}
        >
          👁️ View Story
        </button>
      </nav>

      {/* Generate Tab */}
      {activeTab === 'generate' && (
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Generate New Story</h2>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Story Prompt:</label>
            <textarea
              style={styles.textarea}
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              placeholder="Enter your story idea... (e.g., 'A brave knight discovers a magical library')"
              rows={3}
            />
          </div>
          <button 
            style={{...styles.button, ...styles.primaryButton}}
            onClick={generateStory}
            disabled={isGenerating}
          >
            {isGenerating ? '🔄 Generating...' : '✨ Generate Story'}
          </button>
        </div>
      )}

      {/* Refine Tab */}
      {activeTab === 'refine' && currentStory && (
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Refine Your Images</h2>
          
          {/* Current Images Display */}
          <div style={styles.imageGrid}>
            <div style={styles.imageContainer}>
              <h3 style={styles.imageTitle}>Character</h3>
              {currentStory.character_image_url && (
                <img 
                  src={`http://localhost:8000${currentStory.character_image_url}`}
                  alt="Character"
                  style={styles.image}
                />
              )}
            </div>
            <div style={styles.imageContainer}>
              <h3 style={styles.imageTitle}>Background</h3>
              {currentStory.background_image_url && (
                <img 
                  src={`http://localhost:8000${currentStory.background_image_url}`}
                  alt="Background"
                  style={styles.image}
                />
              )}
            </div>
            <div style={styles.imageContainer}>
              <h3 style={styles.imageTitle}>Combined</h3>
              {currentStory.combined_image_url && (
                <img 
                  src={`http://localhost:8000${currentStory.combined_image_url}`}
                  alt="Combined"
                  style={styles.image}
                />
              )}
            </div>
          </div>

          {/* Individual Refinement Controls */}
          <div style={styles.refinementGrid}>
            {/* Character Refinement */}
            <div style={styles.refinementCard}>
              <h3 style={styles.cardTitle}>🎭 Refine Character</h3>
              <textarea
                style={styles.refinementInput}
                value={refinementPrompts.character}
                onChange={(e) => setRefinementPrompts(prev => ({
                  ...prev, character: e.target.value
                }))}
                placeholder="e.g., 'knight, heroic stance, confident expression, dramatic lighting'"
                rows={2}
              />
              <div style={styles.strengthControl}>
                <label style={styles.strengthLabel}>
                  Strength: {strengthValues.character.toFixed(2)}
                </label>
                <div style={styles.strengthInputContainer}>
                  <input
                    type="range"
                    min="0.1"
                    max="1.0"
                    step="0.05"
                    value={strengthValues.character}
                    onChange={(e) => handleStrengthChange('character', e.target.value)}
                    style={styles.strengthSlider}
                  />
                  <input
                    type="number"
                    min="0.1"
                    max="1.0"
                    step="0.05"
                    value={strengthValues.character}
                    onChange={(e) => handleStrengthChange('character', e.target.value)}
                    style={styles.strengthNumber}
                  />
                </div>
                <div style={styles.strengthHints}>
                  <span style={styles.strengthHint}>0.1 = Subtle</span>
                  <span style={styles.strengthHint}>1.0 = Dramatic</span>
                </div>
              </div>
              <button 
                style={{...styles.button, ...styles.secondaryButton}}
                onClick={refineCharacter}
                disabled={isRefining.character}
              >
                {isRefining.character ? '🔄 Refining...' : '🎨 Refine Character'}
              </button>
            </div>

            {/* Background Refinement */}
            <div style={styles.refinementCard}>
              <h3 style={styles.cardTitle}>🏞️ Refine Background</h3>
              <textarea
                style={styles.refinementInput}
                value={refinementPrompts.background}
                onChange={(e) => setRefinementPrompts(prev => ({
                  ...prev, background: e.target.value
                }))}
                placeholder="e.g., 'castle courtyard, empty center space, organized layout'"
                rows={2}
              />
              <div style={styles.strengthControl}>
                <label style={styles.strengthLabel}>
                  Strength: {strengthValues.background.toFixed(2)}
                </label>
                <div style={styles.strengthInputContainer}>
                  <input
                    type="range"
                    min="0.1"
                    max="1.0"
                    step="0.05"
                    value={strengthValues.background}
                    onChange={(e) => handleStrengthChange('background', e.target.value)}
                    style={styles.strengthSlider}
                  />
                  <input
                    type="number"
                    min="0.1"
                    max="1.0"
                    step="0.05"
                    value={strengthValues.background}
                    onChange={(e) => handleStrengthChange('background', e.target.value)}
                    style={styles.strengthNumber}
                  />
                </div>
                <div style={styles.strengthHints}>
                  <span style={styles.strengthHint}>0.1 = Subtle</span>
                  <span style={styles.strengthHint}>1.0 = Dramatic</span>
                </div>
              </div>
              <button 
                style={{...styles.button, ...styles.secondaryButton}}
                onClick={refineBackground}
                disabled={isRefining.background}
              >
                {isRefining.background ? '🔄 Refining...' : '🎨 Refine Background'}
              </button>
            </div>
          </div>

          {/* Smart Refinement */}
          <div style={styles.smartRefinement}>
            <h3 style={styles.cardTitle}>🧠 Smart Scene Refinement</h3>
            <div style={styles.smartInputs}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Character Adjustments:</label>
                <input
                  style={styles.input}
                  value={refinementPrompts.characterAdjustments}
                  onChange={(e) => setRefinementPrompts(prev => ({
                    ...prev, characterAdjustments: e.target.value
                  }))}
                  placeholder="e.g., 'knight, library lighting, scholarly pose'"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Background Adjustments:</label>
                <input
                  style={styles.input}
                  value={refinementPrompts.backgroundAdjustments}
                  onChange={(e) => setRefinementPrompts(prev => ({
                    ...prev, backgroundAdjustments: e.target.value
                  }))}
                  placeholder="e.g., 'library, knight-scale furniture, reading space'"
                />
              </div>
            </div>
            <div style={styles.strengthControl}>
              <label style={styles.strengthLabel}>
                Smart Refinement Strength: {strengthValues.smart.toFixed(2)}
              </label>
              <div style={styles.strengthInputContainer}>
                <input
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={strengthValues.smart}
                  onChange={(e) => handleStrengthChange('smart', e.target.value)}
                  style={styles.strengthSlider}
                />
                <input
                  type="number"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={strengthValues.smart}
                  onChange={(e) => handleStrengthChange('smart', e.target.value)}
                  style={styles.strengthNumber}
                />
              </div>
              <div style={styles.strengthHints}>
                <span style={styles.strengthHint}>0.1 = Subtle</span>
                <span style={styles.strengthHint}>1.0 = Dramatic</span>
              </div>
            </div>
            <button 
              style={{...styles.button, ...styles.accentButton}}
              onClick={smartRefine}
              disabled={isRefining.smart}
            >
              {isRefining.smart ? '🔄 Smart Refining...' : '✨ Smart Refine Both'}
            </button>
          </div>
        </div>
      )}

      {/* View Tab */}
      {activeTab === 'view' && currentStory && (
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Your Story</h2>
          
          {/* Story Text */}
          <div style={styles.storyContainer}>
            <h3 style={styles.storyTitle}>📖 Story</h3>
            <p style={styles.storyText}>{currentStory.short_story}</p>
          </div>

          {/* Character Description */}
          <div style={styles.descriptionContainer}>
            <h3 style={styles.descriptionTitle}>🎭 Character Description</h3>
            <p style={styles.descriptionText}>{currentStory.character_description}</p>
          </div>

          {/* Background Description */}
          <div style={styles.descriptionContainer}>
            <h3 style={styles.descriptionTitle}>🏞️ Background Description</h3>
            <p style={styles.descriptionText}>{currentStory.background_description}</p>
          </div>

          {/* Final Combined Image */}
          <div style={styles.finalImageContainer}>
            <h3 style={styles.imageTitle}>🎨 Final Scene</h3>
            {currentStory.combined_image_url && (
              <img 
                src={`http://localhost:8000${currentStory.combined_image_url}`}
                alt="Final Combined Scene"
                style={styles.finalImage}
              />
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={styles.footer}>
        <p>Made with ❤️ using Django + LangChain + Stable Diffusion</p>
      </footer>
    </div>
  );
};

// Styles object
const styles = {
  container: {
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
    padding: '20px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  title: {
    color: '#2c3e50',
    fontSize: '2.5rem',
    margin: '0 0 10px 0',
    fontWeight: '700',
  },
  subtitle: {
    color: '#6c757d',
    fontSize: '1.1rem',
    margin: 0,
  },
  error: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    border: '1px solid #f5c6cb',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  errorClose: {
    background: 'none',
    border: 'none',
    fontSize: '20px',
    cursor: 'pointer',
    color: '#721c24',
  },
  nav: {
    display: 'flex',
    gap: '10px',
    marginBottom: '30px',
    backgroundColor: '#ffffff',
    padding: '10px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  tab: {
    flex: 1,
    padding: '12px 24px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: '600',
    transition: 'all 0.3s ease',
    backgroundColor: '#e9ecef',
    color: '#495057',
  },
  activeTab: {
    backgroundColor: '#007bff',
    color: '#ffffff',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
  },
  section: {
    backgroundColor: '#ffffff',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '20px',
  },
  sectionTitle: {
    color: '#2c3e50',
    fontSize: '1.8rem',
    marginBottom: '25px',
    fontWeight: '700',
  },
  inputGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    color: '#495057',
    fontWeight: '600',
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    fontSize: '1rem',
    transition: 'border-color 0.3s ease',
    boxSizing: 'border-box',
  },
  textarea: {
    width: '100%',
    padding: '12px 16px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    fontSize: '1rem',
    transition: 'border-color 0.3s ease',
    resize: 'vertical',
    boxSizing: 'border-box',
  },
  button: {
    padding: '12px 24px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: '600',
    transition: 'all 0.3s ease',
    textAlign: 'center',
  },
  primaryButton: {
    backgroundColor: '#007bff',
    color: '#ffffff',
    boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
  },
  secondaryButton: {
    backgroundColor: '#28a745',
    color: '#ffffff',
    boxShadow: '0 4px 12px rgba(40,167,69,0.3)',
  },
  accentButton: {
    backgroundColor: '#dc3545',
    color: '#ffffff',
    boxShadow: '0 4px 12px rgba(220,53,69,0.3)',
  },
  imageGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  imageContainer: {
    textAlign: 'center',
  },
  imageTitle: {
    color: '#495057',
    fontSize: '1.2rem',
    marginBottom: '10px',
    fontWeight: '600',
  },
  image: {
    width: '100%',
    maxWidth: '200px',
    height: 'auto',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    transition: 'transform 0.3s ease',
  },
  refinementGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  refinementCard: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '10px',
    border: '2px solid #e9ecef',
  },
  cardTitle: {
    color: '#495057',
    fontSize: '1.3rem',
    marginBottom: '15px',
    fontWeight: '600',
  },
  refinementInput: {
    width: '100%',
    padding: '10px 14px',
    border: '2px solid #dee2e6',
    borderRadius: '6px',
    fontSize: '0.95rem',
    marginBottom: '15px',
    resize: 'vertical',
    boxSizing: 'border-box',
  },
  strengthControl: {
    marginBottom: '20px',
    padding: '15px',
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    border: '1px solid #dee2e6',
  },
  strengthLabel: {
    display: 'block',
    marginBottom: '10px',
    color: '#495057',
    fontWeight: '600',
    fontSize: '0.9rem',
  },
  strengthInputContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    marginBottom: '10px',
  },
  strengthSlider: {
    flex: 1,
    height: '6px',
    borderRadius: '3px',
    background: '#dee2e6',
    outline: 'none',
    cursor: 'pointer',
  },
  strengthNumber: {
    width: '80px',
    padding: '6px 10px',
    border: '1px solid #dee2e6',
    borderRadius: '4px',
    fontSize: '0.9rem',
    textAlign: 'center',
  },
  strengthHints: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '0.8rem',
    color: '#6c757d',
  },
  strengthHint: {
    fontStyle: 'italic',
  },
  smartRefinement: {
    padding: '25px',
    backgroundColor: '#f1f3f4',
    borderRadius: '12px',
    border: '2px solid #dee2e6',
  },
  smartInputs: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '20px',
  },
  storyContainer: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '10px',
    marginBottom: '20px',
  },
  storyTitle: {
    color: '#495057',
    fontSize: '1.4rem',
    marginBottom: '15px',
    fontWeight: '600',
  },
  storyText: {
    color: '#212529',
    fontSize: '1.1rem',
    lineHeight: '1.6',
    margin: 0,
  },
  descriptionContainer: {
    backgroundColor: '#f8f9fa',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '15px',
  },
  descriptionTitle: {
    color: '#495057',
    fontSize: '1.2rem',
    marginBottom: '10px',
    fontWeight: '600',
  },
  descriptionText: {
    color: '#495057',
    fontSize: '1rem',
    lineHeight: '1.5',
    margin: 0,
  },
  finalImageContainer: {
    textAlign: 'center',
    marginTop: '30px',
  },
  finalImage: {
    maxWidth: '100%',
    height: 'auto',
    borderRadius: '12px',
    boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
  },
  footer: {
    textAlign: 'center',
    marginTop: '40px',
    padding: '20px',
    color: '#6c757d',
    fontSize: '0.9rem',
  },
};

export default StoryGeneratorApp;