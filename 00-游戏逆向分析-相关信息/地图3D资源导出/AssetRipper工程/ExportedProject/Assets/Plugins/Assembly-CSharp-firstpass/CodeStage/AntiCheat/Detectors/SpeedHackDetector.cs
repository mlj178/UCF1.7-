using System;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CodeStage.AntiCheat.Detectors
{
	[DisallowMultipleComponent]
	public class SpeedHackDetector : ACTkDetectorBase
	{
		internal const string ComponentName = "Speed Hack Detector";

		internal const string LogPrefix = "[ACTk] Speed Hack Detector: ";

		private const long TicksPerSecond = 10000000L;

		private const int Threshold = 5000000;

		private const float ThresholdFloat = 0.5f;

		private static int instancesInScene;

		public float interval;

		public byte maxFalsePositives;

		public int coolDown;

		private byte currentFalsePositives;

		private int currentCooldownShots;

		private long ticksOnStart;

		private long vulnerableTicksOnStart;

		private long previousTicks;

		private long previousIntervalTicks;

		private float vulnerableTimeOnStart;

		public static SpeedHackDetector Instance { get; private set; }

		private static SpeedHackDetector GetOrCreateInstance => null;

		public static SpeedHackDetector AddToSceneOrGetExisting()
		{
			return null;
		}

		public static void StartDetection()
		{
		}

		public static void StartDetection(Action callback)
		{
		}

		public static void StartDetection(Action callback, float interval)
		{
		}

		public static void StartDetection(Action callback, float interval, byte maxFalsePositives)
		{
		}

		public static void StartDetection(Action callback, float interval, byte maxFalsePositives, int coolDown)
		{
		}

		public static void StopDetection()
		{
		}

		public static void Dispose()
		{
		}

		private SpeedHackDetector()
		{
		}

		private void Awake()
		{
		}

		protected override void OnDestroy()
		{
		}

		private void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)
		{
		}

		private void OnApplicationPause(bool pause)
		{
		}

		private void Update()
		{
		}

		private void StartDetectionInternal(Action callback, float checkInterval, byte falsePositives, int shotsTillCooldown)
		{
		}

		protected override void StartDetectionAutomatically()
		{
		}

		protected override void DisposeInternal()
		{
		}

		private void ResetStartTicks()
		{
		}

		private long GetReliableTicks()
		{
			return 0L;
		}
	}
}
