using UnityEngine;

namespace BotAction
{
	public class BA_WantInfected : BotActionBase
	{
		public static float Rate;

		private bool goDie;

		private float nextCheckTime;

		public BA_WantInfected(Bot bot)
			: base(null)
		{
		}

		private void Bot_Destination_Listener(ref Vector3 pos, ref int priority)
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}

		private void UpdateNextCheckTime()
		{
		}

		public static void SetDefaultRate()
		{
		}
	}
}
