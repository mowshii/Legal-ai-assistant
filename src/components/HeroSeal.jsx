/**
 * components/HeroSeal.jsx
 * ---------------------------
 * The page's one deliberate visual flourish: a slowly rotating 3D wax
 * seal built in pure CSS (transform-style: preserve-3d), evoking a
 * notarized/registered legal document rather than a generic gradient
 * blob. No external 3D asset files — see index.css for the keyframes.
 */
import { FileCheck2 } from "lucide-react";

export default function HeroSeal() {
  return (
    <div className="seal-stage flex items-center justify-center">
      <div className="seal-3d">
        <div className="seal-face">
          <div className="seal-ring" />
          <FileCheck2 className="text-parchment" size={72} strokeWidth={1.5} />
        </div>
      </div>
    </div>
  );
}
