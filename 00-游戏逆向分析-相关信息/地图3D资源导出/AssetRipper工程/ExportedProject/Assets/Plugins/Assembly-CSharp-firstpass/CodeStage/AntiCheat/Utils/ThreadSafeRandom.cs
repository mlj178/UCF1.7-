using System;

namespace CodeStage.AntiCheat.Utils
{
	public class ThreadSafeRandom
	{
		private static readonly Random Global;

		[ThreadStatic]
		private static Random local;

		public static int Next(int minInclusive, int maxExclusive)
		{
			return 0;
		}

		public static int Next()
		{
			return 0;
		}

		public static int Next(int maxExclusive)
		{
			return 0;
		}
	}
}
