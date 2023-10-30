import { useState } from "react";

export const useHover = () => {
    const [hovered, setHovered] = useState(false);

    const hoverEventHandlers = {
      onMouseEnter: () => setHovered(true),
      onMouseLeave: () => setHovered(false),
    }

    return {hovered, hoverEventHandlers};
  }