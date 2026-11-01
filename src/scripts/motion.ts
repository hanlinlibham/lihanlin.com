/* 站点动效层：GSAP + ScrollTrigger + Lenis。
   所有隐藏状态都由 JS 设置，脚本失败时页面保持可读。 */
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const root = document.documentElement;
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function grain() {
  const el = document.querySelector<HTMLElement>(".noise");
  if (!el) return;
  const c = document.createElement("canvas");
  c.width = c.height = 180;
  const ctx = c.getContext("2d")!;
  const img = ctx.createImageData(180, 180);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = Math.random() * 255;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
    img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
  el.style.backgroundImage = `url(${c.toDataURL()})`;
}

function boot() {
  if (reduce) { root.classList.add("motion-off"); return; }
  gsap.registerPlugin(ScrollTrigger);
  root.classList.add("js-motion");

  import("lenis").then(({ default: Lenis }) => {
    const lenis = new Lenis({ lerp: 0.08, smoothWheel: true, wheelMultiplier: 0.85 });
    lenis.on("scroll", ScrollTrigger.update);
    const raf = (t: number) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", (e) => {
        const id = a.getAttribute("href")!;
        if (id.length > 1 && document.querySelector(id)) {
          e.preventDefault();
          lenis.scrollTo(id, { offset: -70, duration: 1.1 });
        }
      });
    });
    ScrollTrigger.refresh();
  });

  grain();

  const lines = document.querySelectorAll(".reveal-line > span");
  if (lines.length) {
    gsap.set(lines, { yPercent: 115 });
    gsap.timeline({ delay: 0.12, defaults: { ease: "expo.out" } })
      .to(lines, { yPercent: 0, duration: 1.15, stagger: 0.085 })
      .from(".hero-panel", { opacity: 0, y: 26, duration: 0.85 }, 0.3)
      .from(".hero-cta .btn", { opacity: 0, y: 14, duration: 0.55, stagger: 0.06 }, 0.5)
      .from(".stats > div", { opacity: 0, y: 16, duration: 0.65, stagger: 0.06 }, 0.6)
      .from(".cue", { opacity: 0, duration: 0.5 }, 0.95);
  }

  gsap.to(".hero-panel", {
    yPercent: -7, ease: "none",
    scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
  });

  gsap.utils.toArray<HTMLElement>(".section-head").forEach((head) => {
    const h2 = head.querySelector("h2");
    if (h2) gsap.from(h2, { y: 26, opacity: 0, duration: 0.9, ease: "expo.out",
      scrollTrigger: { trigger: head, start: "top 88%", once: true } });
    const rule = head.querySelector(".rule");
    if (rule) gsap.from(rule, { scaleX: 0, transformOrigin: "left center", duration: 1.1, ease: "expo.inOut",
      scrollTrigger: { trigger: head, start: "top 88%", once: true } });
    ScrollTrigger.create({ trigger: head, start: "top 88%", once: true,
      onEnter: () => head.classList.add("in-view") });
  });

  function reveal(sel: string, o: { y?: number; duration?: number; stagger?: number } = {}) {
    gsap.utils.toArray<HTMLElement>(sel).forEach((el, i) => {
      gsap.set(el, { opacity: 0, y: o.y ?? 28 });
      ScrollTrigger.create({ trigger: el, start: "top 90%", once: true,
        onEnter: () => gsap.to(el, { opacity: 1, y: 0, duration: o.duration ?? 0.8, ease: "expo.out",
          delay: (i % 3) * (o.stagger ?? 0.06) }) });
    });
  }
  reveal(".section-lead, .prose p, .ticks li, .pills li, .community li, .writing li, .facts", { y: 22 });
  reveal(".card-reveal", { y: 34, duration: 0.9, stagger: 0.08 });
  reveal(".note-card", { y: 26, stagger: 0.07 });

  gsap.utils.toArray<HTMLElement>(".stat-num[data-to]").forEach((el) => {
    const to = parseFloat(el.dataset.to || "0");
    const suffix = el.dataset.suffix || "";
    const obj = { v: 0 };
    gsap.to(obj, { v: to, duration: 1.5, ease: "expo.out",
      scrollTrigger: { trigger: el, start: "top 95%", once: true },
      onUpdate: () => { el.textContent = Math.round(obj.v) + suffix; } });
  });

  gsap.utils.toArray<HTMLElement>(".flow").forEach((flow) => {
    gsap.from(flow.children, { opacity: 0, y: 16, duration: 0.55, ease: "power3.out", stagger: 0.07,
      scrollTrigger: { trigger: flow, start: "top 90%", once: true } });
  });

  const bar = document.querySelector<HTMLElement>(".progress i");
  if (bar) {
    const set = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
    };
    set();
    window.addEventListener("scroll", set, { passive: true });
    window.addEventListener("resize", set);
  }
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
