"""
AEGIS Autonomous Background Daemon
Runs continuous background loops, evaluating telemetry, running division routines, and updating posture.
"""

import asyncio
import time
from typing import Optional
from aegis.core.utils import utc_now_iso


class AegisDaemon:
    """
    Continuous background loop runner for AEGIS.
    """

    def __init__(self, orchestrator, interval_seconds: int = 45):
        self.orchestrator = orchestrator
        self.interval_seconds = interval_seconds
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self.total_ticks = 0
        self.last_tick_time: Optional[str] = None

    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.orchestrator.state_mgr.state.loop_active = True
        self.orchestrator.state_mgr._save_state()
        self.orchestrator._log("DAEMON", f"Autonomous Daemon started. Interval: {self.interval_seconds}s")
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        self.orchestrator.state_mgr.state.loop_active = False
        self.orchestrator.state_mgr._save_state()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self.orchestrator._log("DAEMON", "Autonomous Daemon halted.")

    async def _run_loop(self):
        while self.is_running:
            try:
                self.total_ticks += 1
                self.last_tick_time = utc_now_iso()
                
                # Execute single cycle of the Value Creation Loop
                self.orchestrator.execute_single_loop_cycle()

            except Exception as e:
                self.orchestrator._log("DAEMON_ERROR", f"Error in background tick: {str(e)}")

            await asyncio.sleep(self.interval_seconds)

    def get_status(self):
        return {
            "is_running": self.is_running,
            "interval_seconds": self.interval_seconds,
            "total_ticks": self.total_ticks,
            "last_tick_time": self.last_tick_time
        }
